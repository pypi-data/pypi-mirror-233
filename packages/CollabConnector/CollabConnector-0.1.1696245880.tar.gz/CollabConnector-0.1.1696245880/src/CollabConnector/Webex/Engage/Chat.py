import sys


class Chat:
    def __init__(self, parent):
        self.parent = parent

    def list(self, team_id: int = None, status: str = "all") -> dict:
        if status.lower() == "all":
            if chats := self.parent.rest.get(f"/v3.0/chats",
                                             headers={"teamid": str(team_id if team_id else self.parent.team.id)}
                                             ):
                return chats['chats']
        elif status:
            return self.search(search_params={
                "condition": "AND",
                "rules": [
                    {
                        "param_name": "status",
                        "operator": "eq",
                        "param_value": status.lower()
                    }
                ]
            },
                team_id=team_id)
        return {}

    def get(self, chat_id: int, team_id: int = None) -> dict:
        if chat := self.parent.rest.get(f"/v3.0/chats/{chat_id}",
                                        headers={"teamid": str(team_id if team_id else self.parent.team.id)}
                                        ):
            return chat

        print(f"Error getting chat: {chat_id}", file=sys.stderr)
        return {}

    def search(self, search_params: dict = {}, team_id: int = None) -> dict:
        """
        search_params = {
                "condition": "AND",
                "rules": [
                    {
                        "condition": "OR",
                        "rules": [
                            {
                                "param_name": "mobile",
                                "operator": "eq",
                                "param_value": "44739273721"
                            },
                            {
                                "param_name": "facebook_psid",
                                "operator": "eq",
                                "param_value": "12983719823712"
                            }
                        ]
                    },
                    {
                        "param_name": "status",
                        "operator": "not_eq",
                        "param_value": "closed"
                    }
                ]
            }
        """
        if chat := self.parent.rest.post(f"/v3.0/chats/search",
                                         data=search_params
                                         # headers={"teamid": str(team_id if team_id else self.parent.team.id)}
                                         ):
            return chat
        print("Chats not found", file=sys.stderr)
        return {}
