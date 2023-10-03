import argparse
import io
import json
import os
from typing import Any, Dict, List, Union
from urllib.parse import urljoin

import boto3
from dotenv import load_dotenv
from PIL import Image

from functional_cat.registry import ModelMeta

cat_img = Image.open("sample_imgs/cat.jpg")
street_sign_img = Image.open("sample_imgs/street_sign.jpg")
ein_and_friends_img = Image.open("sample_imgs/gang.jpg").convert("RGB")

load_dotenv()

ENDPOINT_URL = os.getenv("ENDPOINT_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")


def upload_img_to_s3(img: Image.Image, model_name: str) -> str:
    f = io.BytesIO()
    img.save(f, format="PNG")
    f.seek(0)

    s3 = boto3.client(
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        verify=False,
    )

    key = f"sample-output/{model_name}.png"

    s3.upload_fileobj(f, Bucket=BUCKET_NAME, Key=key)

    url = urljoin(ENDPOINT_URL, f"{BUCKET_NAME}/{key}")

    return url


catalog_path = "web/src/funcs.json"


def truncate_output(out: Any) -> str:
    ret = str(out)
    if len(ret) > 500:
        ret = ret[:500] + "..."
    return ret


def model_meta_entry(
    model_meta: ModelMeta, fields: List[str] = None, call_kwargs: dict = None
) -> Dict[str, Any]:
    call_kwargs = call_kwargs or {"score_thres": 0.5}

    def create_example(mm: ModelMeta) -> dict:
        model = mm.load_model()
        out = model([mm.example_img], **call_kwargs)
        img_with_preds = model.draw_output_on_img(mm.example_img, out[0])

        return {
            "outputImage": upload_img_to_s3(img_with_preds, model_meta.name),
            "output": truncate_output(out),
        }

    def class_labels(mm: ModelMeta) -> List[str]:
        # todo: make the check for GLIP cleaner
        if mm.class_.__name__ != "GLIP":
            model = mm.load_model()
            if hasattr(model, "class_labels"):
                return model.class_labels

    def key_point_labels(mm: ModelMeta) -> List[str]:
        if mm.class_.__name__ != "GLIP":
            model = mm.load_model()
            if hasattr(model, "key_point_labels"):
                return model.key_point_labels

    key_to_fn = {
        "class": lambda mm: f"{mm.class_.__module__}.{mm.class_.__name__}",
        "constructorArgs": lambda mm: mm.constructor_args,
        "description": lambda mm: mm.description,
        "task": lambda mm: mm.task.value,
        "example": create_example,
        "framework": lambda mm: mm.framework.value,
        "installSnippet": lambda mm: mm.install_snippet,
        "devices": lambda mm: {
            "cpu": mm.cpu_support,
            "gpu": mm.gpu_support,
        },
        "classLabels": class_labels,
        "keyPointLabels": key_point_labels,
        "colabLink": lambda mm: mm.colab_link,
    }

    fields = fields or list(key_to_fn.keys())

    return {k: key_to_fn[k](model_meta) for k in fields}


def create_catalog(
    model_metas: List[ModelMeta],
    overwrite_if_exists: bool,
    fields: Union[List[str], None],
    call_kwargs: List[dict] = None,
) -> None:
    call_kwargs = call_kwargs or [None] * len(model_metas)

    assert len(call_kwargs) == len(model_metas)

    if os.path.exists(catalog_path):
        with open(catalog_path) as f:
            cat = json.load(f)
    else:
        cat = {}

    for model_meta, call_kwargs in zip(model_metas, call_kwargs):
        if model_meta.name in cat and not overwrite_if_exists:
            print(
                f"{model_meta.name} already exists in catalog {catalog_path}, skipping."
            )
            continue
        elif model_meta.name not in cat:
            cat[model_meta.name] = {}

        print(f"processing {model_meta.name}")
        cat[model_meta.name].update(
            model_meta_entry(model_meta, fields, call_kwargs=call_kwargs)
        )

    with open(catalog_path, "w") as f:
        json.dump(cat, f, indent=2)
        f.write("\n")


def delete_entry(name: str):
    with open(catalog_path) as f:
        cat = json.load(f)

    if name in cat:
        cat.pop(name)

        with open(catalog_path, "w") as f:
            json.dump(cat, f, indent=2)
            f.write("\n")
    else:
        print(
            f"model '{name}' not found in catalog at {catalog_path}, nothing to do."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs="*", help="One of create or delete")
    parser.add_argument("--frameworks", type=str)
    parser.add_argument("--fields", type=str)
    parser.add_argument("--overwrite-if-exists", action="store_true")
    args = parser.parse_args()

    action = args.action[0]
    if action == "create":
        # TODO: make this more compatible with functional_cat.registry.Framework
        possible_frameworks = {"torch", "onnx", "glip", "dlib"}
        if args.frameworks is None:
            raise RuntimeError("Must pass --frameworks")
        frameworks = args.frameworks.split(",")
        assert set(frameworks) <= possible_frameworks

        fields = None if args.fields is None else args.fields.split(",")

        for framework in frameworks:
            if framework == "torch":
                from functional_cat.registry import (
                    create_torchvision_model_metas,
                )

                create_catalog(
                    model_metas=create_torchvision_model_metas(
                        detection_example_img=cat_img,
                        keypoint_example_img=ein_and_friends_img,
                    ),
                    overwrite_if_exists=args.overwrite_if_exists,
                    fields=fields,
                )
            elif framework == "onnx":
                from functional_cat.registry import create_onnx_model_metas

                create_catalog(
                    model_metas=create_onnx_model_metas(cat_img),
                    overwrite_if_exists=args.overwrite_if_exists,
                    fields=fields,
                )
            elif framework == "glip":
                from functional_cat.registry import create_glip_model_metas

                create_catalog(
                    model_metas=create_glip_model_metas(cat_img),
                    overwrite_if_exists=args.overwrite_if_exists,
                    fields=fields,
                )
            elif framework == "dlib":
                from functional_cat.registry import create_dlib_model_metas

                create_catalog(
                    model_metas=create_dlib_model_metas(ein_and_friends_img),
                    overwrite_if_exists=args.overwrite_if_exists,
                    fields=fields,
                    call_kwargs=[{"upsample_factor": 2, "score_thres": 0}],
                )

    elif action == "delete":
        for entry_name in args.action[1:]:
            delete_entry(entry_name)
    else:
        raise RuntimeError(f"argument '{action}' not understood.")
