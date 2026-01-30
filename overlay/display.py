def get_prestige_color(level: int) -> str:
    prestige_map = {
        900: '&5',
        800: '&9',
        700: '&d',
        600: '&4',
        500: '&3',
        400: '&2',
        300: '&b',
        200: '&6',
        100: '&f',
        0: '&7',
    }

    prestige_map_2 = {
        1100: ("&7", "&f", "&f", "&f", "&f", "&7", "&7"),
        1000: ("&c", "&6", "&e", "&a", "&b", "&d", "&5"),
    }

    level_str = f"[{level}✫]"

    if level < 1000:
        for threshold in sorted(prestige_map.keys(), reverse=True):
            if level >= threshold:
                color = prestige_map[threshold]
                return "".join(f"{color}{c}" for c in level_str)

    for threshold in sorted(prestige_map_2.keys(), reverse=True):
        if level >= threshold:
            colors = prestige_map_2[threshold]
            return "".join(
                f"{colors[i % len(colors)]}{c}"
                for i, c in enumerate(level_str)
            )

    return "".join(f"&7{c}" for c in level_str)


def get_role_prefix(role: str) -> str:
    role_prefixes = {
        "Owner": " &c[Owner] ",
        "Admin": " &c[Admin] ",
        "Manager": " &4[Manager] ",
        "Dev": " &a[Dev] ",
        "HeadBuilder": " &5[HeadBuilder] ",
        "Builder": " &d[Builder] ",
        "SrMod": " &e[SrMod] ",
        "Mod": " &e[Mod] ",
        "Trainee": " &a[Trainee] ",
        "Youtube": " &c[&fYoutube&c] ",
        "Master": " &6[Master] ",
        "Expert": " &9[Expert] ",
        "Adept": " &2[Adept] ",
        "Legend": " &6[Leg&een&fd&6] ",
    }
    return role_prefixes.get(role, " &7")


def get_displayname(name: str, role: str) -> str:
    if role == "Legend":
        if len(name) >= 3:
            name = '&6' + name[:-3] + '&e' + name[-3:-1] + '&f' + name[-1]
        elif len(name) == 2:
            name = '&6' + name[0] + '&6' + name[1]
        elif len(name) == 1:
            name = '&6' + name

    return f"{get_role_prefix(role)}{name}"
