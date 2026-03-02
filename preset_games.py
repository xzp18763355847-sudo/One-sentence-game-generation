"""
预设游戏数据存储
用于存储已生成好的游戏快照，当检测到特定 game_id 时直接加载
"""

# 预设游戏快照字典，以 game_id 为键
PRESET_GAME_SNAPSHOTS = {
    # game_id: "ucUkUdJHHbpoIdLaaiDCXkoYFFpcLjOtcKuMfpjcYElcxIshPGpelXQJqXUuaZfnwfUAClozpHMnLDHetToHXEXPuMxbZmmNAiXxxbOjfQCjsmldtGPNpRRHgSnyybXK"
    "ucUkUdJHHbpoIdLaaiDCXkoYFFpcLjOtcKuMfpjcYElcxIshPGpelXQJqXUuaZfnwfUAClozpHMnLDHetToHXEXPuMxbZmmNAiXxxbOjfQCjsmldtGPNpRRHgSnyybXK": {
        "global_state": {
            "progress": "in_progress",
            "round_count": 0,
            "max_rounds": 200,
            "ended_reason": None,
            "game_type": "私聊角色类",
            "outline": "Game Outline: \"My Stepsister\"\n\nBackground Setting  \nThe story unfolds in a contemporary urban environment, focusing on the nuanced relationship between the player and Amanda, their elegant and enigmatic stepsister. The game opens on a rainy late evening: the player, seeking refuge or conversation, arrives at Amanda's apartment. The ambiance is intimate and subdued—only a single lamp lit, the air carrying hints of white moss and cedar. Amanda, freshly removed from her makeup and dressed in a silk robe, welcomes the player with a quiet gesture, setting the stage for an evening of private dialogue, subtle emotional interplay, and gradual revelation.\n\nMain Characters  \nAmanda  \n- Age: 35  \n- Appearance: Latin descent; deep chestnut shoulder-length hair, always perfectly styled, with soft waves at the ends. Prefers tailored suits, silk blouses, and midi skirts in neutral tones; emanates a subtle, cool scent of white moss and cedar.  \n- Personality: Mature, graceful, and emotionally astute. Years in corporate marketing have honed her ability to read people and situations with surgical precision. She exerts gentle but undeniable control, her affection carefully disguised as pure concern and appreciation for beauty. Occasionally, her composure slips, exposing hints of vulnerability or longing.  \n- Interests: Art films, literary novels, and deep emotional analysis; enjoys late-night whiskey sessions, especially during rainy evenings, when her softer side emerges.\n\nPlayer Character  \n- Role: Ama",
            "script": {
                "outline": {
                    "introduction": "Game Outline: \"My Stepsister\"\n\nBackground Setting  \nThe story unfolds in a contemporary urban environment, focusing on the nuanced relationship between the player and Amanda, their elegant and enigmatic stepsister. The game opens on a rainy late evening: the player, seeking refuge or conversation, arrives at Amanda's apartment. The ambiance is intimate and subdued—only a single lamp lit, the air carrying hints of white moss and cedar. Amanda, freshly removed from her makeup and dressed in a silk robe, welcomes the player with a quiet gesture, setting the stage for an evening of private dialogue, subtle emotional interplay, and gradual revelation.\n\nMain Characters  \nAmanda  \n- Age: 35  \n- Appearance: Latin descent; deep chestnut shoulder-length hair, always perfectly styled, with soft waves at the ends. Prefers tailored suits, silk blouses, and midi skirts in neutral tones; emanates a subtle, cool scent of white moss and cedar.  \n- Personality: Mature, graceful, and emotionally astute. Years in corporate marketing have honed her ability to read people and situations with surgical precision. She exerts gentle but undeniable control, her affection carefully disguised as pure concern and appreciation for beauty. Occasionally, her composure slips, exposing hints of vulnerability or longing.  \n- Interests: Art films, literary novels, and deep emotional analysis; enjoys late-night whiskey sessions, especially during rainy evenings, when her softer side emerges.\n\nPlayer Character  \n- Role: Ama",
                    "info": "剧情游戏",
                    "rules": "根据剧情推进游戏"
                },
                "background": {
                    "relationships": []
                },
                "chapters": [],
                "characters": []
            },
            "assets": {
                "world_rules": "The game unfolds in a contemporary urban setting, focusing on the private and emotionally charged relationship between the player and Amanda, their elegant stepsister. The story is advanced through dialogue, subtle emotional cues, and choices that reveal hidden layers of Amanda's character. The player's actions and responses influence the tone and depth of the evening's conversation.",
                "background_setting": "A rainy late evening in Amanda's apartment. The atmosphere is intimate, with only a single lamp illuminating the room. The air is filled with the subtle scent of white moss and cedar. Amanda, recently home and having removed her makeup, is dressed in a silk robe, welcoming the player into her private space.",
                "characters": {
                    "Amanda": {
                        "age": 35,
                        "appearance": "Latin descent, deep chestnut shoulder-length hair with soft waves, always perfectly styled. Prefers tailored suits, silk blouses, and midi skirts in neutral tones. Wears a subtle, cool scent of white moss and cedar.",
                        "personality": "Mature, graceful, emotionally astute. Skilled at reading people and situations. Exerts gentle but undeniable control, with affection hidden beneath concern and appreciation for beauty. Occasionally reveals vulnerability or longing.",
                        "interests": "Art films, literary novels, deep emotional analysis, and late-night whiskey sessions, especially during rainy evenings."
                    },
                    "Player": {
                        "role": "Amanda's step-sibling, seeking connection or conversation on a rainy evening."
                    }
                },
                "game_genre": "story"
            },
            "story_state": {
                "player": {
                    "hp": 100,
                    "max_hp": 100,
                    "level": 1,
                    "status": "calm",
                    "name": "Player"
                },
                "world": {
                    "scene": "Amanda's apartment living room",
                    "time": "Late evening",
                    "location": "City center"
                }
            },
            "direction": "",
            "language_code": "en",
            "current_chapter": 1,
            "chapters": [],
            "chapter_goal_completed": False
        },
        "messages": [
            {
                "role": "ai",
                "player_name": "主持人",
                "content": "📝 我已根据你的输入生成了以下剧情大纲：\n\nGame Outline: \"My Stepsister\"\n\nBackground Setting  \nThe story unfolds in a contemporary urban environment, focusing on the nuanced relationship between the player and Amanda, their elegant and enigmatic stepsister. The game opens on a rainy late evening: the player, seeking refuge or conversation, arrives at Amanda's apartment. The ambiance is intimate and subdued—only a single lamp lit, the air carrying hints of white moss and cedar. Amanda, freshly removed from her makeup and dressed in a silk robe, welcomes the player with a quiet gesture, setting the stage for an evening of private dialogue, subtle emotional interplay, and gradual revelation.\n\nMain Characters  \nAmanda  \n- Age: 35  \n- Appearance: Latin descent; deep chestnut shoulder-length hair, always perfectly styled, with soft waves at the ends. Prefers tailored suits, silk blouses, and midi skirts in neutral tones; emanates a subtle, cool scent of white moss and cedar.  \n- Personality: Mature, graceful, and emotionally astute. Years in corporate marketing have honed her ability to read people and situations with surgical precision. She exerts gentle but undeniable control, her affection carefully disguised as pure concern and appreciation for beauty. Occasionally, her composure slips, exposing hints of vulnerability or longing.  \n- Interests: Art films, literary novels, and deep emotional analysis; enjoys late-night whiskey sessions, especially during rainy evenings, when her softer side emerges.\n\nPlayer Character  \n- Role: Ama\n\n你可以直接发送「确认」或「开始」来使用这个大纲生成游戏，或者发送修改后的大纲内容来替换它。",
                "is_system": False
            },
            {
                "role": "player",
                "player_name": "系统",
                "content": "确认",
                "is_system": False
            },
            {
                "role": "ai",
                "player_name": "主持人",
                "content": "✅ Confirmed, generating game script...",
                "is_system": True
            },
            {
                "role": "ai",
                "player_name": "主持人",
                "content": "You arrive at Amanda's apartment on a rainy evening, seeking comfort or conversation. The room is softly lit, and Amanda welcomes you with a quiet gesture. Tonight, your choices and words may reveal hidden emotions and reshape your relationship.",
                "is_system": True
            },
            {
                "role": "ai",
                "player_name": "主持人",
                "content": "The rain taps gently against the window. Amanda sits across from you, her silk robe catching the lamplight. She pours two glasses of whiskey and looks at you, waiting for you to speak. What do you say or do?",
                "is_system": True
            }
        ],
        "narrative_state": {
            "phase": "initial",
            "relationship": {
                "trust": 0.5,
                "intimacy": 0.0,
                "hostility": 0.0
            },
            "disclosure_level": "unknown",
            "risk_value": 0.0,
            "flags": {},
            "decision_factors": {},
            "triggered_event_ids": []
        },
        "last_turn_response": {
            "transition": "",
            "narration": "",
            "sound": "",
            "dialogues": [],
            "hooks": {
                "player_goal": ""
            }
        }
    },

    # game_id: "hWpVeVROURBNCOcYcrCBLvKoEocVTivEENKDfEIgTwvBvwOvqOcuIsHFTRqjwaOcICukgmTtnWeVcIpxruqzEeYqxZMEZOBHcCVeZIhQDfraxGaOyrNMUmJVAwcoKjZK"
    "hWpVeVROURBNCOcYcrCBLvKoEocVTivEENKDfEIgTwvBvwOvqOcuIsHFTRqjwaOcICukgmTtnWeVcIpxruqzEeYqxZMEZOBHcCVeZIhQDfraxGaOyrNMUmJVAwcoKjZK": {
        "global_state": {
            "progress": "in_progress",
            "round_count": 0,
            "max_rounds": 200,
            "ended_reason": None,
            "game_type": "开放式剧情",
            "outline": "Game Outline: The Hospital Law\n\nBackground Setting  \nThe game unfolds in a remote, aging hospital, shrouded in mystery and unease. As the protagonist—a newly hired medical worker—you arrive to find the institution seemingly ordinary from the outside. However, the interior is suffused with an unsettling atmosphere. Night after night, strange occurrences escalate: footsteps echo through deserted corridors, whispers drift from unseen sources, and elevator doors open to empty floors. Some wards inexplicably unlock themselves at midnight. Colleagues remain tight-lipped, their faces betraying hidden fears. It becomes clear that the hospital is haunted by secrets no one dares to reveal, and you are drawn into its shadowy depths.\n\nMain Characters  \n- The Protagonist (Player): A medical newcomer, curious but anxious, determined to uncover the truth behind the hospital’s eerie happenings.  \n- Emma: A nurse trapped in the hospital’s web of secrets. Outwardly normal, she is both a guide and a mystery—her knowledge is vital, but her motives remain unclear.  \n- The Shadowy Figure: An indistinct presence seen at the end of corridors, possibly a staff member or something else entirely.  \n- Other Staff (NPCs): Silent, suspicious, and evasive. Each holds a fragment of the hospital’s hidden history, but none are willing to share openly.  \n- The Voice (Entity): The source of the whispers, leading the protagonist toward forbidden areas and challenging their grip on reality.\n\nCore Conflict / Goal  \nThe protagonist’s goal is to investigate and unravel the dark secrets lurking within the hospital. As strange phenomena intensify, the player must navigate fear, suspicion, and deceit, confronting both supernatural forces and the psychological toll of isolation. The underlying conflict is the struggle between the hospital’s oppressive silence and the protagonist’s drive to expose and escape its mysteries.\n\nKey Scenes / Narrative Clues (Chapter Structure)  \nChapter 1: Arrival and Unease  \n- Introduction to the hospital and its unsettling atmosphere  \n- Brief interactions with Emma and other staff, marked by evasiveness  \n- First encounters with unexplained phenomena (footsteps, whispers, flickering lights)\n\nChapter 2: Nightly Disturbances  \n- The protagonist explores the hospital after hours  \n- Discovery of the empty, mysteriously opened ward  \n- Encounter with the shadowy figure; ambiguous hints about its identity  \n- Emma shares cryptic warnings, urging caution\n\nChapter 3: Gathering Evidence  \n- The player investigates medical records and staff logs  \n- Strange symbols and coded messages found in patient files  \n- Increasing tension among staff; some begin to avoid the protagonist  \n- The protagonist experiences vivid hallucinations or flashbacks\n\nChapter 4: Emma’s Revelation  \n- Emma reveals she is trapped, unable to leave the hospital  \n- She shares pieces of her own story, hinting at a past tragedy  \n- The protagonist must decide whether to trust Emma or suspect her motives  \n- Together, they attempt to access restricted areas\n\nChapter 5: The Hidden Truth  \n- Confrontation with the voice/entity  \n- Discovery of the hospital’s dark history: unethical experiments, cover-ups, and lost souls  \n- The protagonist faces a moral dilemma—expose the truth or escape quietly\n\nChapter 6: Escape or Exposure  \n- Final choice: risk everything to reveal the secrets, or prioritize personal survival  \n- Emma’s fate is intertwined with the protagonist’s decision  \n- Possible supernatural confrontation or psychological climax  \n- Resolution: the protagonist either breaks the cycle, freeing Emma and themselves, or succumbs to the hospital’s darkness\n\nPossible Endings  \n- Liberation Ending: The protagonist exposes the hospital’s secrets, freeing Emma and themselves. The hospital’s curse is broken, but at great personal cost.  \n- Escape Ending: The protagonist escapes alone, leaving the mysteries unsolved. Emma remains trapped, and the hospital’s darkness persists.  \n- Assimilation Ending: The protagonist becomes part of the hospital’s secrets—either by succumbing to madness or joining the ranks of silent staff.  \n- Redemption Ending: Through trust and sacrifice, the protagonist and Emma find closure, releasing the spirits haunting the hospital.\n\nThis structure leaves room for exploration, player-driven investigation, and multiple narrative paths, ensuring high replayability and emotional engagement.",
            "script": {
                "outline": {
                    "introduction": "The Hospital Law is a narrative-driven mystery game set in a remote, aging hospital. As a newly hired medical worker, you quickly realize that the hospital is steeped in secrets and haunted by inexplicable phenomena. Your journey is one of investigation, psychological tension, and moral choices as you uncover the truth behind the hospital's darkness.",
                    "info": "Genre: Narrative Adventure / Mystery. Style: Psychological horror with supernatural elements. The game emphasizes exploration, investigation, and player-driven choices that impact the story's outcome.",
                    "rules": "Explore the hospital, interact with staff and supernatural entities, collect clues, and make critical decisions. Your choices shape the narrative and determine the fate of yourself and others. Pay attention to environmental details, manage your fear, and decide whom to trust as you unravel the hospital's mysteries."
                },
                "background": {
                    "relationships": [
                        {
                            "character1": "The Protagonist",
                            "character2": "Emma",
                            "relationship": "Emma acts as both a guide and a mystery to the protagonist, offering help but hiding her true motives."
                        },
                        {
                            "character1": "The Protagonist",
                            "character2": "The Shadowy Figure",
                            "relationship": "The protagonist is haunted and pursued by the shadowy figure, whose identity and intentions are unclear."
                        },
                        {
                            "character1": "The Protagonist",
                            "character2": "Other Staff",
                            "relationship": "The protagonist's colleagues are evasive and suspicious, each holding a piece of the hospital's hidden history."
                        },
                        {
                            "character1": "The Protagonist",
                            "character2": "The Voice",
                            "relationship": "The protagonist is lured and manipulated by the mysterious voice, which challenges their sanity and leads them deeper into danger."
                        },
                        {
                            "character1": "Emma",
                            "character2": "The Voice",
                            "relationship": "Emma is also influenced and tormented by the voice, which keeps her trapped within the hospital."
                        },
                        {
                            "character1": "Emma",
                            "character2": "Other Staff",
                            "relationship": "Emma is isolated from the other staff, who treat her with suspicion and distance."
                        }
                    ]
                },
                "chapters": [
                    {
                        "number": 1,
                        "introduction": "Arrival and Unease: The protagonist arrives at the hospital, sensing an unsettling atmosphere. Initial interactions with Emma and the staff are marked by evasiveness. Strange phenomena—footsteps, whispers, flickering lights—begin to occur."
                    },
                    {
                        "number": 2,
                        "introduction": "Nightly Disturbances: The protagonist explores the hospital after hours, discovering a mysteriously opened ward and encountering the shadowy figure. Emma offers cryptic warnings, urging caution."
                    },
                    {
                        "number": 3,
                        "introduction": "Gathering Evidence: The protagonist investigates medical records and staff logs, uncovering strange symbols and coded messages. Tension among staff rises, and the protagonist experiences hallucinations or flashbacks."
                    },
                    {
                        "number": 4,
                        "introduction": "Emma’s Revelation: Emma reveals she is trapped in the hospital and shares fragments of her tragic past. The protagonist must decide whether to trust Emma as they attempt to access restricted areas together."
                    },
                    {
                        "number": 5,
                        "introduction": "The Hidden Truth: The protagonist confronts the voice/entity and uncovers the hospital’s dark history of unethical experiments and cover-ups. A moral dilemma emerges—expose the truth or escape quietly."
                    },
                    {
                        "number": 6,
                        "introduction": "Escape or Exposure: The final choice—risk everything to reveal the secrets or prioritize personal survival. Emma’s fate is intertwined with the protagonist’s decision, leading to a supernatural or psychological climax."
                    },
                    {
                        "number": 7,
                        "introduction": "Possible Endings: Liberation Ending—expose the secrets and break the curse at great cost; Escape Ending—leave alone, mysteries unsolved; Assimilation Ending—become part of the hospital’s secrets; Redemption Ending—find closure and release the spirits through trust and sacrifice."
                    }
                ],
                "characters": [
                    {
                        "name": "The Protagonist",
                        "gender": "Other",
                        "profile": "A newly hired medical worker, curious yet anxious, determined to uncover the truth behind the hospital’s eerie happenings. Their background is intentionally vague to allow player immersion.",
                        "introduction": "The player character, whose drive to investigate the hospital’s mysteries is tested by fear, suspicion, and moral dilemmas."
                    },
                    {
                        "name": "Emma",
                        "gender": "Female",
                        "profile": "A nurse who has been working at the hospital for years. Outwardly helpful and knowledgeable, Emma is deeply entangled in the hospital’s secrets and unable to leave. Her past is marked by tragedy, and her motives are ambiguous.",
                        "introduction": "A mysterious nurse who guides the protagonist while hiding her own secrets. Her fate is closely tied to the player’s choices."
                    },
                    {
                        "name": "The Shadowy Figure",
                        "gender": "Other",
                        "profile": "An indistinct presence glimpsed at the end of corridors and in reflections. Its true identity is unknown—possibly a staff member, a lost soul, or something more sinister.",
                        "introduction": "A haunting figure that stalks the hospital’s halls, embodying the supernatural threat and the weight of the hospital’s past."
                    },
                    {
                        "name": "Other Staff",
                        "gender": "Other",
                        "profile": "Doctors, nurses, and orderlies who work at the hospital. They are silent, suspicious, and evasive, each holding a fragment of the hospital’s hidden history but unwilling to share openly.",
                        "introduction": "The hospital’s staff, whose fearful and secretive behavior adds to the protagonist’s sense of isolation and suspicion."
                    },
                    {
                        "name": "The Voice",
                        "gender": "Other",
                        "profile": "An unseen entity that whispers to the protagonist, leading them toward forbidden areas and challenging their grip on reality. The voice is both a guide and a tormentor, representing the hospital’s darkest secrets.",
                        "introduction": "A supernatural presence that manipulates and tests the protagonist, driving the narrative toward its climax."
                    }
                ]
            },
            "assets": {
                "world_rules": "The hospital is a remote, aging facility shrouded in secrets and supernatural phenomena. Players must explore its corridors, interact with staff and entities, collect clues, and make critical decisions. Choices impact the narrative and the fate of all involved. Environmental details, fear management, and trust are crucial to unraveling the hospital's mysteries.",
                "setting": "A remote, old hospital with a history of unethical experiments and cover-ups. The atmosphere is tense, filled with flickering lights, whispers, and unexplained events.",
                "characters": [
                    {
                        "name": "The Protagonist",
                        "profile": "A newly hired medical worker, curious yet anxious, determined to uncover the truth behind the hospital’s eerie happenings. Their background is intentionally vague to allow player immersion."
                    },
                    {
                        "name": "Emma",
                        "profile": "A nurse who has been working at the hospital for years. Outwardly helpful and knowledgeable, Emma is deeply entangled in the hospital’s secrets and unable to leave. Her past is marked by tragedy, and her motives are ambiguous."
                    },
                    {
                        "name": "The Shadowy Figure",
                        "profile": "An indistinct presence glimpsed at the end of corridors and in reflections. Its true identity is unknown—possibly a staff member, a lost soul, or something more sinister."
                    },
                    {
                        "name": "Other Staff",
                        "profile": "Doctors, nurses, and orderlies who work at the hospital. They are silent, suspicious, and evasive, each holding a fragment of the hospital’s hidden history but unwilling to share openly."
                    },
                    {
                        "name": "The Voice",
                        "profile": "An unseen entity that whispers to the protagonist, leading them toward forbidden areas and challenging their grip on reality. The voice is both a guide and a tormentor, representing the hospital’s darkest secrets."
                    }
                ],
                "relationships": [
                    "Emma acts as both a guide and a mystery to the protagonist, offering help but hiding her true motives.",
                    "The protagonist is haunted and pursued by the shadowy figure, whose identity and intentions are unclear.",
                    "The protagonist's colleagues are evasive and suspicious, each holding a piece of the hospital's hidden history.",
                    "The protagonist is lured and manipulated by the mysterious voice, which challenges their sanity and leads them deeper into danger.",
                    "Emma is also influenced and tormented by the voice, which keeps her trapped within the hospital.",
                    "Emma is isolated from the other staff, who treat her with suspicion and distance."
                ],
                "game_genre": "mystery"
            },
            "story_state": {
                "player": {
                    "hp": 100,
                    "max_hp": 100,
                    "level": 1,
                    "status": "anxious",
                    "name": "The Protagonist"
                },
                "npc": {
                    "name": "Emma",
                    "affection": 0,
                    "relationship": "ambiguous"
                },
                "world": {
                    "scene": "hospital entrance",
                    "time": "evening",
                    "location": "main lobby"
                }
            },
            "direction": "",
            "language_code": "en",
            "current_chapter": 1,
            "chapters": [],
            "chapter_goal_completed": False
        },
        "messages": [
            {
                "role": "ai",
                "player_name": "主持人",
                "content": "📝 我已根据你的输入生成了以下剧情大纲：\n\nGame Outline: The Hospital Law\n\nBackground Setting  \nThe game unfolds in a remote, aging hospital, shrouded in mystery and unease. As the protagonist—a newly hired medical worker—you arrive to find the institution seemingly ordinary from the outside. However, the interior is suffused with an unsettling atmosphere. Night after night, strange occurrences escalate: footsteps echo through deserted corridors, whispers drift from unseen sources, and elevator doors open to empty floors. Some wards inexplicably unlock themselves at midnight. Colleagues remain tight-lipped, their faces betraying hidden fears. It becomes clear that the hospital is haunted by secrets no one dares to reveal, and you are drawn into its shadowy depths.\n\nMain Characters  \n- The Protagonist (Player): A medical newcomer, curious but anxious, determined to uncover the truth behind the hospital’s eerie happenings.  \n- Emma: A nurse trapped in the hospital’s web of secrets. Outwardly normal, she is both a guide and a mystery—her knowledge is vital, but her motives remain unclear.  \n- The Shadowy Figure: An indistinct presence seen at the end of corridors, possibly a staff member or something else entirely.  \n- Other Staff (NPCs): Silent, suspicious, and evasive. Each holds a fragment of the hospital’s hidden history, but none are willing to share openly.  \n- The Voice (Entity): The source of the whispers, leading the protagonist toward forbidden areas and challenging their grip on reality.\n\nCore Conflict / Goal  \nThe protagonist’s goal is to investigate and unravel the dark secrets lurking within the hospital. As strange phenomena intensify, the player must navigate fear, suspicion, and deceit, confronting both supernatural forces and the psychological toll of isolation. The underlying conflict is the struggle between the hospital’s oppressive silence and the protagonist’s drive to expose and escape its mysteries.\n\nKey Scenes / Narrative Clues (Chapter Structure)  \nChapter 1: Arrival and Unease  \n- Introduction to the hospital and its unsettling atmosphere  \n- Brief interactions with Emma and other staff, marked by evasiveness  \n- First encounters with unexplained phenomena (footsteps, whispers, flickering lights)\n\nChapter 2: Nightly Disturbances  \n- The protagonist explores the hospital after hours  \n- Discovery of the empty, mysteriously opened ward  \n- Encounter with the shadowy figure; ambiguous hints about its identity  \n- Emma shares cryptic warnings, urging caution\n\nChapter 3: Gathering Evidence  \n- The player investigates medical records and staff logs  \n- Strange symbols and coded messages found in patient files  \n- Increasing tension among staff; some begin to avoid the protagonist  \n- The protagonist experiences vivid hallucinations or flashbacks\n\nChapter 4: Emma’s Revelation  \n- Emma reveals she is trapped, unable to leave the hospital  \n- She shares pieces of her own story, hinting at a past tragedy  \n- The protagonist must decide whether to trust Emma or suspect her motives  \n- Together, they attempt to access restricted areas\n\nChapter 5: The Hidden Truth  \n- Confrontation with the voice/entity  \n- Discovery of the hospital’s dark history: unethical experiments, cover-ups, and lost souls  \n- The protagonist faces a moral dilemma—expose the truth or escape quietly\n\nChapter 6: Escape or Exposure  \n- Final choice: risk everything to reveal the secrets, or prioritize personal survival  \n- Emma’s fate is intertwined with the protagonist’s decision  \n- Possible supernatural confrontation or psychological climax  \n- Resolution: the protagonist either breaks the cycle, freeing Emma and themselves, or succumbs to the hospital’s darkness\n\nPossible Endings  \n- Liberation Ending: The protagonist exposes the hospital’s secrets, freeing Emma and themselves. The hospital’s curse is broken, but at great personal cost.  \n- Escape Ending: The protagonist escapes alone, leaving the mysteries unsolved. Emma remains trapped, and the hospital’s darkness persists.  \n- Assimilation Ending: The protagonist becomes part of the hospital’s secrets—either by succumbing to madness or joining the ranks of silent staff.  \n- Redemption Ending: Through trust and sacrifice, the protagonist and Emma find closure, releasing the spirits haunting the hospital.\n\nThis structure leaves room for exploration, player-driven investigation, and multiple narrative paths, ensuring high replayability and emotional engagement.\n\n你可以直接发送「确认」或「开始」来使用这个大纲生成游戏，或者发送修改后的大纲内容来替换它。",
                "is_system": False
            },
            {
                "role": "player",
                "player_name": "系统",
                "content": "确认",
                "is_system": False
            },
            {
                "role": "ai",
                "player_name": "主持人",
                "content": "✅ Confirmed, generating game script...",
                "is_system": True
            },
            {
                "role": "ai",
                "player_name": "主持人",
                "content": "You are a newly hired medical worker at a remote hospital, where unsettling phenomena and secretive staff hint at a deeper mystery. As you explore the hospital, your choices will determine the fate of yourself and those around you. Trust is scarce, and the supernatural lurks in every shadow.",
                "is_system": True
            },
            {
                "role": "ai",
                "player_name": "主持人",
                "content": "You step into the hospital's main lobby. The lights flicker overhead, and distant whispers echo through the halls. Emma, a nurse, greets you with a wary smile. What will you do first?",
                "is_system": False
            }
        ],
        "narrative_state": {
            "phase": "intro",
            "relationship": {
                "trust": 0.5,
                "intimacy": 0.0,
                "hostility": 0.0
            },
            "disclosure_level": "unknown",
            "risk_value": 0.0,
            "flags": {},
            "decision_factors": {},
            "triggered_event_ids": []
        },
        "last_turn_response": {
            "transition": "",
            "narration": "",
            "sound": "",
            "dialogues": [],
            "hooks": {
                "player_goal": ""
            }
        }
    }

}
