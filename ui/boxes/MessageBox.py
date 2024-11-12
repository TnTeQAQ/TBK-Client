import dearpygui.dearpygui as dpg
from ui.boxes import Box
import utils.Utils as utils


class MessageBox(Box):
    def draw(self):
        with dpg.window(label="Message", tag=f"message_window"):
            message_data = utils.build_message_tree(self._tbk_data.message_data["pubs"])
            message_list_collapsing_header = dpg.add_collapsing_header(
                label="Message List"
            )
            for puuid in message_data:
                node_name_tree_node = dpg.add_tree_node(label=puuid, parent=message_list_collapsing_header)
                for uuid in message_data[puuid]:
                    msg_info = message_data[puuid][uuid].ep_info
                    node_name = msg_info.node_name
                    name = msg_info.name
                    msg_name = msg_info.msg_name
                    msg_type = msg_info.msg_type
                    msg_type_url = msg_info.msg_type_url
                    
                    msg_name_checkbox = dpg.add_checkbox(
                        label=f"{msg_name}({name})", parent=node_name_tree_node
                    )
                    user_data = {
                        "msg_name": msg_name,
                        "name": name,
                        "msg_type": msg_type,
                        "uuid": uuid,
                        "puuid":puuid
                    }
                    with dpg.drag_payload(
                        parent=msg_name_checkbox,
                        payload_type="plot_data",
                        drag_data=user_data,
                    ):
                        dpg.add_text(f"{puuid}_payload")





        # with dpg.window(label="Message", tag=f"message_window"):
        #     message_data = self._tbk_data.message_data
        #     pubs = message_data["pubs"]
        # with dpg.collapsing_header(label="Message List", tag=f"{dpg.generate_uuid()}_treenode"):
        #     item = []
        #     message_tree = utils.build_message_tree(pubs)
        #     for puuid, node_name in message_tree.items():
        #         for theme_name, node_msgs in node_name.items():
        #             with dpg.tree_node(label=f"{theme_name}({puuid})", tag=f"{puuid}_treenode"):
        #                 for msg, messages in node_msgs.items():
        #                     with dpg.tree_node(label=msg, tag=f"{puuid}_{msg}_treenode"):
        #                         for msg_name in messages:
        #                             with dpg.group(tag=f"{puuid}_{msg}_{msg_name}_group", horizontal=True):
        #                                 uuid = f"{puuid}_{msg}_{msg_name}_group"
        #                                 user_data = {
        #                                     'msg': msg,
        #                                     'name': msg_name,
        #                                     'type': 'TBK_Message',
        #                                     'uuid': uuid,
        #                                 }
        #                                 dpg.add_checkbox(label=msg_name, tag=f"{uuid}_checkbox",

        #                                                  user_data=(msg_name, uuid))
        #                                 with dpg.drag_payload(parent=f"{uuid}_checkbox", payload_type="plot_data",
        #                                                       drag_data=user_data):
        #                                     dpg.add_text(f"{uuid}_payload")
        #                                 dpg.add_spacer(width=80)
        #                                 dpg.add_text(tag=f"{uuid}_text", default_value="")

    def update(self):
        pass
        # dpg.does_alias_exist()

        # message_data = self._tbk_data.message_data
        # pubs = message_data["pubs"]
        # message_tree = utils.build_message_tree(pubs)
        # for puuid, node_name in message_tree.items():
        #     dpg.configure_item(label=publisher,tag=f"{dpg.generate_uuid()}_treenode")
        #     # print(dpg.get_item_configuration(f"{puuid}_treenode"))

        # message_data = self._tbk_data.message_data
        # pubs = message_data["pubs"]
        # item = []
        # message_tree = utils.build_message_tree(pubs)
        # for puuid, node_name in message_tree.items():
        #     for theme_name, node_msgs in node_name.items():
        #         print(f"{puuid}_treenode:", dpg.get_item_configuration(f"{puuid}_treenode"))
        #         for publisher, messages in node_msgs.items():
        #             # f"{puuid}_{publisher}_treenode"
        #             print(f"{puuid}_{publisher}_treenode:", dpg.get_item_configuration(f"{puuid}_{publisher}_treenode"))
        #
        #             for msg in messages:
        #                 # f"{puuid}_{publisher}_{msg}_group"
        #                 print(f"{puuid}_{publisher}_{msg}_group", dpg.get_item_configuration(f"{puuid}_{publisher}_{msg}_group"))
        #
        #                 uuid = f"{puuid}_{publisher}_{msg}_group"
        #                 # print(uuid)
        #                 dpg.set_item_user_data(f"{uuid}_checkbox", (msg, uuid))

        # dpg.add_spacer(_width=80)
        # dpg.add_text(tag=f"{uuid}_text", default_value="")

        # exit(0)

        # message_data = self._tbk_data.message_data
        # pubs = message_data["pubs"]
        # with dpg.collapsing_header(label="Message List", tag=f"{dpg.generate_uuid()}_treenode"):
        #     item = []
        #     message_tree = utils.build_message_tree(pubs)