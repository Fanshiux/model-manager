from scripts.lib import civitai_util

import gradio as gr
from modules import script_callbacks, generation_parameters_copypaste


def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as model_manager_interface:
        with gr.Tab("Civitai"):
            with gr.Row():
                with gr.Column(scale=1):
                    model_id_tb = gr.Textbox(label="Model Id", info="The identifier for the model",
                                             elem_id="model_id_tb")
                    limit_num = gr.Slider(1, 20, 20, label="Limit",
                                          info="The number of results to be returned per page. This can be a number between 1 and 200. By default, each page will return 100 results",
                                          elem_id="limit_sd")
                    page_num = gr.Number(label="Page", value=1, info="The page from which to start fetching models",
                                         elem_id="page_num")
                    search_tb = gr.Textbox(label="Search", placeholder="Search query to filter models by name",
                                           elem_id="search_tb")
                    tag_tb = gr.Textbox(label="Tag", placeholder="Search query to filter models by tag",
                                        elem_id="tag_tb")
                    username_tb = gr.Textbox(label="User Name", placeholder="Search query to filter models by user",
                                             elem_id="username_tb")
                    types_rd = gr.Radio(
                        ["Checkpoint", "TextualInversion", "Hypernetwork", "AestheticGradient", "LORA", "Controlnet",
                         "Poses"],
                        label="Types",
                        info="The type of model you want to filter with. If none is specified, it will return all types",
                        elem_id="types_rd"
                    )
                    sort_rd = gr.Radio(["Highest Rated", "Most Downloaded", "Newest"],
                                       label="Sort",
                                       info="The order in which you wish to sort the results",
                                       value="Highest Rated",
                                       elem_id="sort_rd")
                    period_rd = gr.Radio(["AllTime", "Year", "Month", "Week", "Day"],
                                         label="Period",
                                         info="The time frame in which the models will be sorted",
                                         value="AllTime",
                                         elem_id="period_rd")
                    with gr.Accordion("More Filter Options", open=False):
                        rating_num = gr.Slider(0, 5, 0, label="Rating",
                                               info="The rating you wish to filter the models with. If none is specified, it will return models with any rating",
                                               elem_id="rating_num")
                        favorites_ckb = gr.Checkbox(label="Favorites",
                                                    info="Filter to favorites of the authenticated user (this requires an API token or session cookie)",
                                                    elem_id="favorites_ckb")
                        hidden_ckb = gr.Checkbox(label="Hidden",
                                                 info="Filter to hidden models of the authenticated user (this requires an API token or session cookie)",
                                                 elem_id="hidden_ckb")
                        primary_file_only_ckb = gr.Checkbox(label="Primary File Only",
                                                            info="Only include the primary file for each model (This will use your preferred format options if you use an API token or session cookie)",
                                                            elem_id="primary_file_only_ckb")
                        allow_no_credit_ckb = gr.Checkbox(label="No Credit",
                                                          info="Filter to models that require or don't require crediting the creator",
                                                          elem_id="allow_no_credit_ckb")
                        allow_derivatives_ckb = gr.Checkbox(label="Derivatives",
                                                            info="Filter to models that allow or don't allow creating derivatives",
                                                            elem_id="allow_derivatives_ckb")
                        allow_different_licenses_ckb = gr.Checkbox(label="Favorites",
                                                                   info="Filter to models that allow or don't allow derivatives to have a different license",
                                                                   elem_id="allow_different_licenses_ckb")
                        allow_commercial_use_rd = gr.Radio(["None", "Image", "Rent", "Sell"],
                                                           label="Commercial Permissions",
                                                           info="Filter to models based on their commercial permissions",
                                                           elem_id="allow_commercial_use_rd")
                with gr.Column(scale=3):
                    get_models_list_btn = gr.Button("Get Models List", variant="primary")
                    models_list_tb = gr.JSON(label="Models List")
            get_models_list_inputs = [
                model_id_tb, limit_num, page_num, search_tb, tag_tb, username_tb, types_rd, sort_rd, period_rd,
                rating_num, favorites_ckb, hidden_ckb, primary_file_only_ckb, allow_no_credit_ckb, allow_derivatives_ckb,
                allow_different_licenses_ckb, allow_commercial_use_rd
            ]
            get_models_list_btn.click(civitai_util.get_models_list, inputs=get_models_list_inputs, outputs=[models_list_tb])
        with gr.Tab("Images"):
            with gr.Row():
                with gr.Column(scale=1):
                    gen_img_info = gr.Button("Gen Image Info", variant="primary")
                    civitai_image_url = gr.Textbox(label="Civitai Image Url")
                    download_image = gr.Checkbox(label="Download Image", value=True)
                    is_civitai = gr.Checkbox(label="Civitai Image", value=True)
                    with gr.Row():
                        send_to_buttons = generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
                with gr.Column(scale=2):
                    img_preview = gr.Image()
                    img_file_info = gr.Textbox(label="Image File Info", interactive=False)

        gen_img_info.click(civitai_util.get_image_and_info_by_image_url, inputs=[civitai_image_url, download_image, is_civitai], outputs=[img_preview, img_file_info])
        generation_parameters_copypaste.bind_buttons(send_to_buttons, img_preview, img_file_info)
    return [(model_manager_interface, "Model Manager", "model_manager")]


script_callbacks.on_ui_tabs(on_ui_tabs)
