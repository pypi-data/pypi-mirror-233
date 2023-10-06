"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
from vhcs.service import ims
from . import template, order

log = logging.getLogger(__name__)


def process(data: dict, state: dict) -> dict:
    org_id = data["orgId"]
    provider_id = state["output"]["myProvider"]["id"]
    images = ims.helper.get_images_by_provider_instance_with_asset_details(provider_id, org_id)

    if not images:
        raise Exception(
            "Failed to create default orders with infra images for org " + org_id + " provider_id " + provider_id
        )

    _create_default_order(org_id, state, images, multi_session=True)
    _create_default_order(org_id, state, images, multi_session=False)


def _create_default_order(org_id: str, state: dict, images: dict, multi_session: str):
    template_type = "MULTI_SESSION" if multi_session else "FLOATING"
    selected_image = None
    for image in images:
        if image["multiSession"] == multi_session:
            selected_image = image
            break

    if not selected_image:
        raise Exception("Failed to create default order for template: " + template_type)

    order_data = template.get("v1/tenant-order.var.yml")["var"]
    order_data["orgId"] = org_id
    order_data["providerInstanceId"] = state["output"]["myProvider"]["id"]
    order_data["edgeDeploymentId"] = state["output"]["myEdge"]["id"]
    order_data["application"]["info"] = []
    order_data["template"]["type"] = template_type
    order_data["image"]["streamId"] = selected_image["id"]

    if selected_image["markers"]:
        order_data["image"]["markerId"] = selected_image["markers"][0]["id"]

    if selected_image["_assetDetails"]:
        order_data["image"]["sku"] = selected_image["_assetDetails"]["data"]["vmSize"]

    order_type = state["deploymentId"] + "-default-" + template_type
    order.add({order_type: order_data})
    log.info("Successfully created order type '%s'", order_type)


def destroy(data: dict, state: dict, force: bool):
    all_orders = order.get()
    orders = {k: v for k, v in all_orders.items() if k != "deleted"}
    if not orders:
        return

    for order_type in orders.keys():
        if order_type.startswith(state["deploymentId"] + "-default-"):
            order.remove(order_type)


def eta(action: str, data: dict, state: dict):
    return "1m"
