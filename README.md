# [EM Slack Tableflip](http://dev.erinmorelli.com/slack/flip)
Flip some tables on [Slack](https://slack.com).

Built using emojis from [here](http://www.emoticonfun.org/flip/) and [here](http://emojicons.com/table-flipping).

----------
## Setup

1. Add a new **Slash Command** by going to:

        https://{your-team}.slack.com/services/new/slash-commands

2. Use one of the following options as your new command:

        /flip
        /fliptable
        /tableflip
        /flip_table
        /table_flip

    **Note:** Table flipping will not work without one of these specific slash commands.

3. Set the **URL** field to:

        http://dev.erinmorelli.com/slack/flip/table

4. Set the **Method** option to `POST`

5. Some optional, but useful extra steps:
    1. Check the box next to **Show this command in the autocomplete list**.
    2. Set the **Description** field to `"Flip some tables"`.
    3. Set the **Usage** hint field to `"[type] (or 'help', 'list')"`.
    4. Set the **Descriptive Label** field to `"EM Slack Tableflip"`.

6. And finally, click the **Save Integration** button. Check out the [usage](#usage) section to get started flipping!

----------
## Usage

**Note:** These examples use `/flip` as the slash command, but yours may vary based on what you selected for step 2 during the [setup](#setup) process.

Use command `/flip help` to view this usage information from within Slack.

**Basic Flip:**

    /flip

**Word Flips:**

    /flip word [word]

**Tip:** You can enter one or multiple words, e.g. `/flip` word hello world produces: `(╯°□°)╯︵ plɹoM ollǝH`

**Special Flips:**

    /flip [type]

Available flip types:

    /flip
        (╯°□°)╯︵ ┻━┻

    /flip battle
        (╯°□°)╯︵ ┻━┻ ︵ ╯(°□° ╯)

    /flip bear
        ʕノ•ᴥ•ʔノ ︵ ┻━┻

    /flip cry
        (╯'□')╯︵ ┻━┻

    /flip cute
        ┻━┻ ︵ ლ(⌒-⌒ლ)

    /flip force
        (._.) ~ ︵ ┻━┻

    /flip freakout
        (ﾉಥДಥ)ﾉ︵┻━┻･/

    /flip jake
        (┛❍ᴥ❍﻿)┛彡┻━┻

    /flip laptop
        (ノÒ益Ó)ノ彡▔▔▏

    /flip magic
        (/¯◡ ‿ ◡)/¯ ~ ┻━┻

    /flip monocle
        (╯ಠ_ರೃ)╯︵ ┻━┻

    /flip opposite
        ノ┬─┬ノ ︵ ( \o°o)\

    /flip owl
        (ʘ∇ʘ)ク 彡 ┻━┻

    /flip people
        (/ .□.)\ ︵╰(゜Д゜)╯︵ /(.□. \)

    /flip person
        (╯°□°）╯︵ /(.□. \)

    /flip pudgy
        (ノ ゜Д゜)ノ ︵ ┻━┻

    /flip rage
        (ﾉಥ益ಥ）ﾉ﻿ ┻━┻

    /flip relax
        ┬─┬ノ( º _ ºノ)

    /flip return
        (ノ^_^)ノ┻━┻ ┬─┬ ノ( ^_^ノ)

    /flip robot
        ┗[© ♒ ©]┛ ︵ ┻━┻

    /flip shrug
        ┻━┻ ︵﻿ ¯\(ツ)/¯ ︵ ┻━┻

    /flip strong
        /(ò.ó)┛彡┻━┻

    /flip teeth
        (ノಠ益ಠ)ノ彡┻━┻

    /flip two
        ┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻

    /flip whoops
        ┬──┬﻿ ¯\_(ツ)

    /flip yelling
        (┛◉Д◉)┛彡┻━┻

Use command `/flip list` to view this list from within Slack.