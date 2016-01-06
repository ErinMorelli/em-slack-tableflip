# [EM Slack Tableflip](https://slack-tableflip.herokuapp.com)
Flip some tables on [Slack](https://slack.com).

Built using emojis from [here](http://www.emoticonfun.org/flip/), [here](http://emojicons.com/table-flipping), and [here](http://tableflipping.com/).

----------
## Quick Setup

[Click here](https://slack-tableflip.herokuapp.com/#quick-setup) for quick setup with Slack.

----------
## Manual Setup

1. Manually add a new slash command to your team by going to:

        https://{your-team}.slack.com/apps/build/custom-integration

    and selecting the **Slash Commands** option.

2. Use one of the following options as your new command:

        /flip
        /fliptable
        /tableflip
        /flip_table
        /table_flip

    **Note:** Table flipping will not work without one of these specific slash commands.

3. Set the **URL** field to:

        https://slack-tableflip.herokuapp.com

4. Set the **Method** option to `POST`

5. Some optional, but useful extra steps:
    1. Check the box next to **Show this command in the autocomplete list**.
    2. Set the **Description** field to `"Flip some tables"`.
    3. Set the **Usage** hint field to `"[type] (or 'help', 'list')"`.
    4. Set the **Descriptive Label** field to `"EM Slack Tableflip"`.

6. And finally, click the **Save Integration** button. Check out the [usage](#usage) section to get started flipping!

----------
## Usage

**Note:** These examples use `/tableflip` as the slash command, but yours may vary based on what you selected for step 2 during a [manual](#manual-setup) setup.

Use command `/tableflip help` to view this usage information from within Slack.

**Basic Flip:**

    /tableflip

**Word Flips:**

    /tableflip word [word]

    /tableflip relax [word]

**Tip:** You can enter one or multiple words, e.g. `/tableflip` word Hello World produces: `(╯°□°)╯︵ plɹoM ollǝH`

**Special Flips:**

    /tableflip [type]

Available flip types:

    /tableflip
        (╯°□°)╯︵ ┻━┻

    /tableflip adorable
        (づ｡◕‿‿◕｡)づ ︵ ┻━┻

    /tableflip battle
        (╯°□°)╯︵ ┻━┻ ︵ ╯(°□° ╯)

    /tableflip bear
        ʕノ•ᴥ•ʔノ ︵ ┻━┻

    /tableflip bomb
        ( ・_・)ノ⌒●~*

    /tableflip bored
        (ノ゜-゜)ノ ︵ ┻━┻

    /tableflip buffet
        (╯°□°）╯︵ ┻━━━┻

    /tableflip cry
        (╯'□')╯︵ ┻━┻

    /tableflip cute
        ┻━┻ ︵ ლ(⌒-⌒ლ)

    /tableflip dead
        (╯°□°）╯︵ /(x_x)|

    /tableflip force
        (._.) ~ ︵ ┻━┻

    /tableflip freakout
        (ﾉಥДಥ)ﾉ︵┻━┻･/

    /tableflip fury
        ┻━┻彡 ヽ(ಠДಠ)ノ彡┻━┻﻿

    /tableflip glare
        (╯ಠ_ಠ）╯︵ ┳━┳

    /tableflip hypnotic
        (╯°.°）╯ ┻━┻

    /tableflip jake
        (┛❍ᴥ❍﻿)┛彡┻━┻

    /tableflip laptop
        (ノÒ益Ó)ノ彡▔▔▏

    /tableflip magic
        (/¯◡ ‿ ◡)/¯ ~ ┻━┻

    /tableflip monocle
        (╯ಠ_ರೃ)╯︵ ┻━┻

    /tableflip opposite
        ノ┬─┬ノ ︵ ( \o°o)\

    /tableflip owl
        (ʘ∇ʘ)ク 彡 ┻━┻

    /tableflip people
        (/ .□.)\ ︵╰(゜Д゜)╯︵ /(.□. \)

    /tableflip person
        (╯°□°）╯︵ /(.□. \)

    /tableflip pudgy
        (ノ ゜Д゜)ノ ︵ ┻━┻

    /tableflip rage
        (ﾉಥ益ಥ）ﾉ﻿ ┻━┻

    /tableflip relax
        ┬─┬ノ( º _ ºノ)

    /tableflip return
        (ノ^_^)ノ┻━┻ ┬─┬ ノ( ^_^ノ)

    /tableflip robot
        ┗[© ♒ ©]┛ ︵ ┻━┻

    /tableflip shrug
        ┻━┻ ︵﻿ ¯\(ツ)/¯ ︵ ┻━┻

    /tableflip strong
        /(ò.ó)┛彡┻━┻

    /tableflip teeth
        (ノಠ益ಠ)ノ彡┻━┻

    /tableflip tantrum
        ┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻

    /tableflip two
        ┻━┻ ︵╰(°□°)╯︵ ┻━┻

    /tableflip whoops
        ┬──┬﻿ ¯\_(ツ)

    /tableflip yelling
        (┛◉Д◉)┛彡┻━┻

Use command `/tableflip list` to view this list from within Slack.