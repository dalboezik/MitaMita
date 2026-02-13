"""Temporäre Daten & Metadaten"""

'''
ticket_context = {
    "<channel_id>": {
        "ticket": disnake.Message(<ticket_message>)
        "ticket_author_id": int(<id>),
        "ticket_mod_id": int(<id>)
    }
}
'''
ticket_context: dict[dict] = {}
'''
voice_channels = {
    int(<voice_channel_id>): disnake.Member(<voice_channel_author>)
}
'''
voice_channels: dict = {}
