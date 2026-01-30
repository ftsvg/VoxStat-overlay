MC_COLORS = {
    "&0": "#000000",
    "&1": "#0000AA",
    "&2": "#00AA00",
    "&3": "#00AAAA",
    "&4": "#AA0000",
    "&5": "#AA00AA",
    "&6": "#FFAA00",
    "&7": "#AAAAAA",
    "&8": "#555555",
    "&9": "#5555FF",
    "&a": "#55FF55",
    "&b": "#55FFFF",
    "&c": "#FF5555",
    "&d": "#FF55FF",
    "&e": "#FFFF55",
    "&f": "#FFFFFF",
}

def mc_to_html(text: str) -> str:
    html = ""
    color = "#FFFFFF"
    i = 0

    while i < len(text):
        if text[i] == "&" and i + 1 < len(text):
            code = text[i:i+2]
            if code in MC_COLORS:
                color = MC_COLORS[code]
                i += 2
                continue
        html += f'<span style="color:{color}">{text[i]}</span>'
        i += 1

    return html
