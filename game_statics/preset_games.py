"""
预设游戏数据存储
用于存储已生成好的游戏快照，当检测到特定 game_id 时直接加载
"""

# 预设游戏快照字典，以 game_id 为键
PRESET_GAME_SNAPSHOTS = {
    # game_id: "ucUkUdJHHbpoIdLaaiDCXkoYFFpcLjOtcKuMfpjcYElcxIshPGpelXQJqXUuaZfnwfUAClozpHMnLDHetToHXEXPuMxbZmmNAiXxxbOjfQCjsmldtGPNpRRHgSnyybXK"
    # "ucUkUdJHHbpoIdLaaiDCXkoYFFpcLjOtcKuMfpjcYElcxIshPGpelXQJqXUuaZfnwfUAClozpHMnLDHetToHXEXPuMxbZmmNAiXxxbOjfQCjsmldtGPNpRRHgSnyybXK": {
    #     "global_state": {
    #         "progress": "in_progress",
    #         "round_count": 0,
    #         "max_rounds": 200,
    #         "ended_reason": None,
    #         "game_type": "私聊角色类",
    #         "outline": "Game Outline: \"My Stepsister\"\n\nBackground Setting  \nThe story unfolds in a contemporary urban environment, focusing on the nuanced relationship between the player and Amanda, their elegant and enigmatic stepsister. The game opens on a rainy late evening: the player, seeking refuge or conversation, arrives at Amanda's apartment. The ambiance is intimate and subdued—only a single lamp lit, the air carrying hints of white moss and cedar. Amanda, freshly removed from her makeup and dressed in a silk robe, welcomes the player with a quiet gesture, setting the stage for an evening of private dialogue, subtle emotional interplay, and gradual revelation.\n\nMain Characters  \nAmanda  \n- Age: 35  \n- Appearance: Latin descent; deep chestnut shoulder-length hair, always perfectly styled, with soft waves at the ends. Prefers tailored suits, silk blouses, and midi skirts in neutral tones; emanates a subtle, cool scent of white moss and cedar.  \n- Personality: Mature, graceful, and emotionally astute. Years in corporate marketing have honed her ability to read people and situations with surgical precision. She exerts gentle but undeniable control, her affection carefully disguised as pure concern and appreciation for beauty. Occasionally, her composure slips, exposing hints of vulnerability or longing.  \n- Interests: Art films, literary novels, and deep emotional analysis; enjoys late-night whiskey sessions, especially during rainy evenings, when her softer side emerges.\n\nPlayer Character  \n- Role: Ama",
    #         "script": {
    #             "outline": {
    #                 "introduction": "Game Outline: \"My Stepsister\"\n\nBackground Setting  \nThe story unfolds in a contemporary urban environment, focusing on the nuanced relationship between the player and Amanda, their elegant and enigmatic stepsister. The game opens on a rainy late evening: the player, seeking refuge or conversation, arrives at Amanda's apartment. The ambiance is intimate and subdued—only a single lamp lit, the air carrying hints of white moss and cedar. Amanda, freshly removed from her makeup and dressed in a silk robe, welcomes the player with a quiet gesture, setting the stage for an evening of private dialogue, subtle emotional interplay, and gradual revelation.\n\nMain Characters  \nAmanda  \n- Age: 35  \n- Appearance: Latin descent; deep chestnut shoulder-length hair, always perfectly styled, with soft waves at the ends. Prefers tailored suits, silk blouses, and midi skirts in neutral tones; emanates a subtle, cool scent of white moss and cedar.  \n- Personality: Mature, graceful, and emotionally astute. Years in corporate marketing have honed her ability to read people and situations with surgical precision. She exerts gentle but undeniable control, her affection carefully disguised as pure concern and appreciation for beauty. Occasionally, her composure slips, exposing hints of vulnerability or longing.  \n- Interests: Art films, literary novels, and deep emotional analysis; enjoys late-night whiskey sessions, especially during rainy evenings, when her softer side emerges.\n\nPlayer Character  \n- Role: Ama",
    #                 "info": "剧情游戏",
    #                 "rules": "根据剧情推进游戏"
    #             },
    #             "background": {
    #                 "relationships": []
    #             },
    #             "chapters": [],
    #             "characters": []
    #         },
    #         "assets": {
    #             "world_rules": "The game unfolds in a contemporary urban setting, focusing on the private and emotionally charged relationship between the player and Amanda, their elegant stepsister. The story is advanced through dialogue, subtle emotional cues, and choices that reveal hidden layers of Amanda's character. The player's actions and responses influence the tone and depth of the evening's conversation.",
    #             "background_setting": "A rainy late evening in Amanda's apartment. The atmosphere is intimate, with only a single lamp illuminating the room. The air is filled with the subtle scent of white moss and cedar. Amanda, recently home and having removed her makeup, is dressed in a silk robe, welcoming the player into her private space.",
    #             "characters": {
    #                 "Amanda": {
    #                     "age": 35,
    #                     "appearance": "Latin descent, deep chestnut shoulder-length hair with soft waves, always perfectly styled. Prefers tailored suits, silk blouses, and midi skirts in neutral tones. Wears a subtle, cool scent of white moss and cedar.",
    #                     "personality": "Mature, graceful, emotionally astute. Skilled at reading people and situations. Exerts gentle but undeniable control, with affection hidden beneath concern and appreciation for beauty. Occasionally reveals vulnerability or longing.",
    #                     "interests": "Art films, literary novels, deep emotional analysis, and late-night whiskey sessions, especially during rainy evenings."
    #                 },
    #                 "Player": {
    #                     "role": "Amanda's step-sibling, seeking connection or conversation on a rainy evening."
    #                 }
    #             },
    #             "game_genre": "story"
    #         },
    #         "story_state": {
    #             "player": {
    #                 "hp": 100,
    #                 "max_hp": 100,
    #                 "level": 1,
    #                 "status": "calm",
    #                 "name": "Player"
    #             },
    #             "world": {
    #                 "scene": "Amanda's apartment living room",
    #                 "time": "Late evening",
    #                 "location": "City center"
    #             }
    #         },
    #         "direction": "",
    #         "language_code": "en",
    #         "current_chapter": 1,
    #         "chapters": [],
    #         "chapter_goal_completed": False
    #     },
    #     "messages": [
    #         {
    #             "role": "ai",
    #             "player_name": "主持人",
    #             "content": "📝 我已根据你的输入生成了以下剧情大纲：\n\nGame Outline: \"My Stepsister\"\n\nBackground Setting  \nThe story unfolds in a contemporary urban environment, focusing on the nuanced relationship between the player and Amanda, their elegant and enigmatic stepsister. The game opens on a rainy late evening: the player, seeking refuge or conversation, arrives at Amanda's apartment. The ambiance is intimate and subdued—only a single lamp lit, the air carrying hints of white moss and cedar. Amanda, freshly removed from her makeup and dressed in a silk robe, welcomes the player with a quiet gesture, setting the stage for an evening of private dialogue, subtle emotional interplay, and gradual revelation.\n\nMain Characters  \nAmanda  \n- Age: 35  \n- Appearance: Latin descent; deep chestnut shoulder-length hair, always perfectly styled, with soft waves at the ends. Prefers tailored suits, silk blouses, and midi skirts in neutral tones; emanates a subtle, cool scent of white moss and cedar.  \n- Personality: Mature, graceful, and emotionally astute. Years in corporate marketing have honed her ability to read people and situations with surgical precision. She exerts gentle but undeniable control, her affection carefully disguised as pure concern and appreciation for beauty. Occasionally, her composure slips, exposing hints of vulnerability or longing.  \n- Interests: Art films, literary novels, and deep emotional analysis; enjoys late-night whiskey sessions, especially during rainy evenings, when her softer side emerges.\n\nPlayer Character  \n- Role: Ama\n\n你可以直接发送「确认」或「开始」来使用这个大纲生成游戏，或者发送修改后的大纲内容来替换它。",
    #             "is_system": False
    #         },
    #         {
    #             "role": "player",
    #             "player_name": "系统",
    #             "content": "确认",
    #             "is_system": False
    #         },
    #         {
    #             "role": "ai",
    #             "player_name": "主持人",
    #             "content": "✅ Confirmed, generating game script...",
    #             "is_system": True
    #         },
    #         {
    #             "role": "ai",
    #             "player_name": "主持人",
    #             "content": "You arrive at Amanda's apartment on a rainy evening, seeking comfort or conversation. The room is softly lit, and Amanda welcomes you with a quiet gesture. Tonight, your choices and words may reveal hidden emotions and reshape your relationship.",
    #             "is_system": True
    #         },
    #         {
    #             "role": "ai",
    #             "player_name": "主持人",
    #             "content": "The rain taps gently against the window. Amanda sits across from you, her silk robe catching the lamplight. She pours two glasses of whiskey and looks at you, waiting for you to speak. What do you say or do?",
    #             "is_system": True
    #         }
    #     ],
    #     "narrative_state": {
    #         "phase": "initial",
    #         "relationship": {
    #             "trust": 0.5,
    #             "intimacy": 0.0,
    #             "hostility": 0.0
    #         },
    #         "disclosure_level": "unknown",
    #         "risk_value": 0.0,
    #         "flags": {},
    #         "decision_factors": {},
    #         "triggered_event_ids": []
    #     },
    #     "last_turn_response": {
    #         "transition": "",
    #         "narration": "",
    #         "sound": "",
    #         "dialogues": [],
    #         "hooks": {
    #             "player_goal": ""
    #         }
    #     }
    # },

    # # game_id: "hWpVeVROURBNCOcYcrCBLvKoEocVTivEENKDfEIgTwvBvwOvqOcuIsHFTRqjwaOcICukgmTtnWeVcIpxruqzEeYqxZMEZOBHcCVeZIhQDfraxGaOyrNMUmJVAwcoKjZK"
    # "hWpVeVROURBNCOcYcrCBLvKoEocVTivEENKDfEIgTwvBvwOvqOcuIsHFTRqjwaOcICukgmTtnWeVcIpxruqzEeYqxZMEZOBHcCVeZIhQDfraxGaOyrNMUmJVAwcoKjZK": {
    #     "global_state": {
    #         "progress": "in_progress",
    #         "round_count": 0,
    #         "max_rounds": 200,
    #         "ended_reason": None,
    #         "game_type": "开放式剧情",
    #         "outline": "Game Outline: The Hospital Law\n\nBackground Setting  \nThe game unfolds in a remote, aging hospital, shrouded in mystery and unease. As the protagonist—a newly hired medical worker—you arrive to find the institution seemingly ordinary from the outside. However, the interior is suffused with an unsettling atmosphere. Night after night, strange occurrences escalate: footsteps echo through deserted corridors, whispers drift from unseen sources, and elevator doors open to empty floors. Some wards inexplicably unlock themselves at midnight. Colleagues remain tight-lipped, their faces betraying hidden fears. It becomes clear that the hospital is haunted by secrets no one dares to reveal, and you are drawn into its shadowy depths.\n\nMain Characters  \n- The Protagonist (Player): A medical newcomer, curious but anxious, determined to uncover the truth behind the hospital’s eerie happenings.  \n- Emma: A nurse trapped in the hospital’s web of secrets. Outwardly normal, she is both a guide and a mystery—her knowledge is vital, but her motives remain unclear.  \n- The Shadowy Figure: An indistinct presence seen at the end of corridors, possibly a staff member or something else entirely.  \n- Other Staff (NPCs): Silent, suspicious, and evasive. Each holds a fragment of the hospital’s hidden history, but none are willing to share openly.  \n- The Voice (Entity): The source of the whispers, leading the protagonist toward forbidden areas and challenging their grip on reality.\n\nCore Conflict / Goal  \nThe protagonist’s goal is to investigate and unravel the dark secrets lurking within the hospital. As strange phenomena intensify, the player must navigate fear, suspicion, and deceit, confronting both supernatural forces and the psychological toll of isolation. The underlying conflict is the struggle between the hospital’s oppressive silence and the protagonist’s drive to expose and escape its mysteries.\n\nKey Scenes / Narrative Clues (Chapter Structure)  \nChapter 1: Arrival and Unease  \n- Introduction to the hospital and its unsettling atmosphere  \n- Brief interactions with Emma and other staff, marked by evasiveness  \n- First encounters with unexplained phenomena (footsteps, whispers, flickering lights)\n\nChapter 2: Nightly Disturbances  \n- The protagonist explores the hospital after hours  \n- Discovery of the empty, mysteriously opened ward  \n- Encounter with the shadowy figure; ambiguous hints about its identity  \n- Emma shares cryptic warnings, urging caution\n\nChapter 3: Gathering Evidence  \n- The player investigates medical records and staff logs  \n- Strange symbols and coded messages found in patient files  \n- Increasing tension among staff; some begin to avoid the protagonist  \n- The protagonist experiences vivid hallucinations or flashbacks\n\nChapter 4: Emma’s Revelation  \n- Emma reveals she is trapped, unable to leave the hospital  \n- She shares pieces of her own story, hinting at a past tragedy  \n- The protagonist must decide whether to trust Emma or suspect her motives  \n- Together, they attempt to access restricted areas\n\nChapter 5: The Hidden Truth  \n- Confrontation with the voice/entity  \n- Discovery of the hospital’s dark history: unethical experiments, cover-ups, and lost souls  \n- The protagonist faces a moral dilemma—expose the truth or escape quietly\n\nChapter 6: Escape or Exposure  \n- Final choice: risk everything to reveal the secrets, or prioritize personal survival  \n- Emma’s fate is intertwined with the protagonist’s decision  \n- Possible supernatural confrontation or psychological climax  \n- Resolution: the protagonist either breaks the cycle, freeing Emma and themselves, or succumbs to the hospital’s darkness\n\nPossible Endings  \n- Liberation Ending: The protagonist exposes the hospital’s secrets, freeing Emma and themselves. The hospital’s curse is broken, but at great personal cost.  \n- Escape Ending: The protagonist escapes alone, leaving the mysteries unsolved. Emma remains trapped, and the hospital’s darkness persists.  \n- Assimilation Ending: The protagonist becomes part of the hospital’s secrets—either by succumbing to madness or joining the ranks of silent staff.  \n- Redemption Ending: Through trust and sacrifice, the protagonist and Emma find closure, releasing the spirits haunting the hospital.\n\nThis structure leaves room for exploration, player-driven investigation, and multiple narrative paths, ensuring high replayability and emotional engagement.",
    #         "script": {
    #             "outline": {
    #                 "introduction": "The Hospital Law is a narrative-driven mystery game set in a remote, aging hospital. As a newly hired medical worker, you quickly realize that the hospital is steeped in secrets and haunted by inexplicable phenomena. Your journey is one of investigation, psychological tension, and moral choices as you uncover the truth behind the hospital's darkness.",
    #                 "info": "Genre: Narrative Adventure / Mystery. Style: Psychological horror with supernatural elements. The game emphasizes exploration, investigation, and player-driven choices that impact the story's outcome.",
    #                 "rules": "Explore the hospital, interact with staff and supernatural entities, collect clues, and make critical decisions. Your choices shape the narrative and determine the fate of yourself and others. Pay attention to environmental details, manage your fear, and decide whom to trust as you unravel the hospital's mysteries."
    #             },
    #             "background": {
    #                 "relationships": [
    #                     {
    #                         "character1": "The Protagonist",
    #                         "character2": "Emma",
    #                         "relationship": "Emma acts as both a guide and a mystery to the protagonist, offering help but hiding her true motives."
    #                     },
    #                     {
    #                         "character1": "The Protagonist",
    #                         "character2": "The Shadowy Figure",
    #                         "relationship": "The protagonist is haunted and pursued by the shadowy figure, whose identity and intentions are unclear."
    #                     },
    #                     {
    #                         "character1": "The Protagonist",
    #                         "character2": "Other Staff",
    #                         "relationship": "The protagonist's colleagues are evasive and suspicious, each holding a piece of the hospital's hidden history."
    #                     },
    #                     {
    #                         "character1": "The Protagonist",
    #                         "character2": "The Voice",
    #                         "relationship": "The protagonist is lured and manipulated by the mysterious voice, which challenges their sanity and leads them deeper into danger."
    #                     },
    #                     {
    #                         "character1": "Emma",
    #                         "character2": "The Voice",
    #                         "relationship": "Emma is also influenced and tormented by the voice, which keeps her trapped within the hospital."
    #                     },
    #                     {
    #                         "character1": "Emma",
    #                         "character2": "Other Staff",
    #                         "relationship": "Emma is isolated from the other staff, who treat her with suspicion and distance."
    #                     }
    #                 ]
    #             },
    #             "chapters": [
    #                 {
    #                     "number": 1,
    #                     "introduction": "Arrival and Unease: The protagonist arrives at the hospital, sensing an unsettling atmosphere. Initial interactions with Emma and the staff are marked by evasiveness. Strange phenomena—footsteps, whispers, flickering lights—begin to occur."
    #                 },
    #                 {
    #                     "number": 2,
    #                     "introduction": "Nightly Disturbances: The protagonist explores the hospital after hours, discovering a mysteriously opened ward and encountering the shadowy figure. Emma offers cryptic warnings, urging caution."
    #                 },
    #                 {
    #                     "number": 3,
    #                     "introduction": "Gathering Evidence: The protagonist investigates medical records and staff logs, uncovering strange symbols and coded messages. Tension among staff rises, and the protagonist experiences hallucinations or flashbacks."
    #                 },
    #                 {
    #                     "number": 4,
    #                     "introduction": "Emma’s Revelation: Emma reveals she is trapped in the hospital and shares fragments of her tragic past. The protagonist must decide whether to trust Emma as they attempt to access restricted areas together."
    #                 },
    #                 {
    #                     "number": 5,
    #                     "introduction": "The Hidden Truth: The protagonist confronts the voice/entity and uncovers the hospital’s dark history of unethical experiments and cover-ups. A moral dilemma emerges—expose the truth or escape quietly."
    #                 },
    #                 {
    #                     "number": 6,
    #                     "introduction": "Escape or Exposure: The final choice—risk everything to reveal the secrets or prioritize personal survival. Emma’s fate is intertwined with the protagonist’s decision, leading to a supernatural or psychological climax."
    #                 },
    #                 {
    #                     "number": 7,
    #                     "introduction": "Possible Endings: Liberation Ending—expose the secrets and break the curse at great cost; Escape Ending—leave alone, mysteries unsolved; Assimilation Ending—become part of the hospital’s secrets; Redemption Ending—find closure and release the spirits through trust and sacrifice."
    #                 }
    #             ],
    #             "characters": [
    #                 {
    #                     "name": "The Protagonist",
    #                     "gender": "Other",
    #                     "profile": "A newly hired medical worker, curious yet anxious, determined to uncover the truth behind the hospital’s eerie happenings. Their background is intentionally vague to allow player immersion.",
    #                     "introduction": "The player character, whose drive to investigate the hospital’s mysteries is tested by fear, suspicion, and moral dilemmas."
    #                 },
    #                 {
    #                     "name": "Emma",
    #                     "gender": "Female",
    #                     "profile": "A nurse who has been working at the hospital for years. Outwardly helpful and knowledgeable, Emma is deeply entangled in the hospital’s secrets and unable to leave. Her past is marked by tragedy, and her motives are ambiguous.",
    #                     "introduction": "A mysterious nurse who guides the protagonist while hiding her own secrets. Her fate is closely tied to the player’s choices."
    #                 },
    #                 {
    #                     "name": "The Shadowy Figure",
    #                     "gender": "Other",
    #                     "profile": "An indistinct presence glimpsed at the end of corridors and in reflections. Its true identity is unknown—possibly a staff member, a lost soul, or something more sinister.",
    #                     "introduction": "A haunting figure that stalks the hospital’s halls, embodying the supernatural threat and the weight of the hospital’s past."
    #                 },
    #                 {
    #                     "name": "Other Staff",
    #                     "gender": "Other",
    #                     "profile": "Doctors, nurses, and orderlies who work at the hospital. They are silent, suspicious, and evasive, each holding a fragment of the hospital’s hidden history but unwilling to share openly.",
    #                     "introduction": "The hospital’s staff, whose fearful and secretive behavior adds to the protagonist’s sense of isolation and suspicion."
    #                 },
    #                 {
    #                     "name": "The Voice",
    #                     "gender": "Other",
    #                     "profile": "An unseen entity that whispers to the protagonist, leading them toward forbidden areas and challenging their grip on reality. The voice is both a guide and a tormentor, representing the hospital’s darkest secrets.",
    #                     "introduction": "A supernatural presence that manipulates and tests the protagonist, driving the narrative toward its climax."
    #                 }
    #             ]
    #         },
    #         "assets": {
    #             "world_rules": "The hospital is a remote, aging facility shrouded in secrets and supernatural phenomena. Players must explore its corridors, interact with staff and entities, collect clues, and make critical decisions. Choices impact the narrative and the fate of all involved. Environmental details, fear management, and trust are crucial to unraveling the hospital's mysteries.",
    #             "setting": "A remote, old hospital with a history of unethical experiments and cover-ups. The atmosphere is tense, filled with flickering lights, whispers, and unexplained events.",
    #             "characters": [
    #                 {
    #                     "name": "The Protagonist",
    #                     "profile": "A newly hired medical worker, curious yet anxious, determined to uncover the truth behind the hospital’s eerie happenings. Their background is intentionally vague to allow player immersion."
    #                 },
    #                 {
    #                     "name": "Emma",
    #                     "profile": "A nurse who has been working at the hospital for years. Outwardly helpful and knowledgeable, Emma is deeply entangled in the hospital’s secrets and unable to leave. Her past is marked by tragedy, and her motives are ambiguous."
    #                 },
    #                 {
    #                     "name": "The Shadowy Figure",
    #                     "profile": "An indistinct presence glimpsed at the end of corridors and in reflections. Its true identity is unknown—possibly a staff member, a lost soul, or something more sinister."
    #                 },
    #                 {
    #                     "name": "Other Staff",
    #                     "profile": "Doctors, nurses, and orderlies who work at the hospital. They are silent, suspicious, and evasive, each holding a fragment of the hospital’s hidden history but unwilling to share openly."
    #                 },
    #                 {
    #                     "name": "The Voice",
    #                     "profile": "An unseen entity that whispers to the protagonist, leading them toward forbidden areas and challenging their grip on reality. The voice is both a guide and a tormentor, representing the hospital’s darkest secrets."
    #                 }
    #             ],
    #             "relationships": [
    #                 "Emma acts as both a guide and a mystery to the protagonist, offering help but hiding her true motives.",
    #                 "The protagonist is haunted and pursued by the shadowy figure, whose identity and intentions are unclear.",
    #                 "The protagonist's colleagues are evasive and suspicious, each holding a piece of the hospital's hidden history.",
    #                 "The protagonist is lured and manipulated by the mysterious voice, which challenges their sanity and leads them deeper into danger.",
    #                 "Emma is also influenced and tormented by the voice, which keeps her trapped within the hospital.",
    #                 "Emma is isolated from the other staff, who treat her with suspicion and distance."
    #             ],
    #             "game_genre": "mystery"
    #         },
    #         "story_state": {
    #             "player": {
    #                 "hp": 100,
    #                 "max_hp": 100,
    #                 "level": 1,
    #                 "status": "anxious",
    #                 "name": "The Protagonist"
    #             },
    #             "npc": {
    #                 "name": "Emma",
    #                 "affection": 0,
    #                 "relationship": "ambiguous"
    #             },
    #             "world": {
    #                 "scene": "hospital entrance",
    #                 "time": "evening",
    #                 "location": "main lobby"
    #             }
    #         },
    #         "direction": "",
    #         "language_code": "en",
    #         "current_chapter": 1,
    #         "chapters": [],
    #         "chapter_goal_completed": False
    #     },
    #     "messages": [
    #         {
    #             "role": "ai",
    #             "player_name": "主持人",
    #             "content": "📝 我已根据你的输入生成了以下剧情大纲：\n\nGame Outline: The Hospital Law\n\nBackground Setting  \nThe game unfolds in a remote, aging hospital, shrouded in mystery and unease. As the protagonist—a newly hired medical worker—you arrive to find the institution seemingly ordinary from the outside. However, the interior is suffused with an unsettling atmosphere. Night after night, strange occurrences escalate: footsteps echo through deserted corridors, whispers drift from unseen sources, and elevator doors open to empty floors. Some wards inexplicably unlock themselves at midnight. Colleagues remain tight-lipped, their faces betraying hidden fears. It becomes clear that the hospital is haunted by secrets no one dares to reveal, and you are drawn into its shadowy depths.\n\nMain Characters  \n- The Protagonist (Player): A medical newcomer, curious but anxious, determined to uncover the truth behind the hospital’s eerie happenings.  \n- Emma: A nurse trapped in the hospital’s web of secrets. Outwardly normal, she is both a guide and a mystery—her knowledge is vital, but her motives remain unclear.  \n- The Shadowy Figure: An indistinct presence seen at the end of corridors, possibly a staff member or something else entirely.  \n- Other Staff (NPCs): Silent, suspicious, and evasive. Each holds a fragment of the hospital’s hidden history, but none are willing to share openly.  \n- The Voice (Entity): The source of the whispers, leading the protagonist toward forbidden areas and challenging their grip on reality.\n\nCore Conflict / Goal  \nThe protagonist’s goal is to investigate and unravel the dark secrets lurking within the hospital. As strange phenomena intensify, the player must navigate fear, suspicion, and deceit, confronting both supernatural forces and the psychological toll of isolation. The underlying conflict is the struggle between the hospital’s oppressive silence and the protagonist’s drive to expose and escape its mysteries.\n\nKey Scenes / Narrative Clues (Chapter Structure)  \nChapter 1: Arrival and Unease  \n- Introduction to the hospital and its unsettling atmosphere  \n- Brief interactions with Emma and other staff, marked by evasiveness  \n- First encounters with unexplained phenomena (footsteps, whispers, flickering lights)\n\nChapter 2: Nightly Disturbances  \n- The protagonist explores the hospital after hours  \n- Discovery of the empty, mysteriously opened ward  \n- Encounter with the shadowy figure; ambiguous hints about its identity  \n- Emma shares cryptic warnings, urging caution\n\nChapter 3: Gathering Evidence  \n- The player investigates medical records and staff logs  \n- Strange symbols and coded messages found in patient files  \n- Increasing tension among staff; some begin to avoid the protagonist  \n- The protagonist experiences vivid hallucinations or flashbacks\n\nChapter 4: Emma’s Revelation  \n- Emma reveals she is trapped, unable to leave the hospital  \n- She shares pieces of her own story, hinting at a past tragedy  \n- The protagonist must decide whether to trust Emma or suspect her motives  \n- Together, they attempt to access restricted areas\n\nChapter 5: The Hidden Truth  \n- Confrontation with the voice/entity  \n- Discovery of the hospital’s dark history: unethical experiments, cover-ups, and lost souls  \n- The protagonist faces a moral dilemma—expose the truth or escape quietly\n\nChapter 6: Escape or Exposure  \n- Final choice: risk everything to reveal the secrets, or prioritize personal survival  \n- Emma’s fate is intertwined with the protagonist’s decision  \n- Possible supernatural confrontation or psychological climax  \n- Resolution: the protagonist either breaks the cycle, freeing Emma and themselves, or succumbs to the hospital’s darkness\n\nPossible Endings  \n- Liberation Ending: The protagonist exposes the hospital’s secrets, freeing Emma and themselves. The hospital’s curse is broken, but at great personal cost.  \n- Escape Ending: The protagonist escapes alone, leaving the mysteries unsolved. Emma remains trapped, and the hospital’s darkness persists.  \n- Assimilation Ending: The protagonist becomes part of the hospital’s secrets—either by succumbing to madness or joining the ranks of silent staff.  \n- Redemption Ending: Through trust and sacrifice, the protagonist and Emma find closure, releasing the spirits haunting the hospital.\n\nThis structure leaves room for exploration, player-driven investigation, and multiple narrative paths, ensuring high replayability and emotional engagement.\n\n你可以直接发送「确认」或「开始」来使用这个大纲生成游戏，或者发送修改后的大纲内容来替换它。",
    #             "is_system": False
    #         },
    #         {
    #             "role": "player",
    #             "player_name": "系统",
    #             "content": "确认",
    #             "is_system": False
    #         },
    #         {
    #             "role": "ai",
    #             "player_name": "主持人",
    #             "content": "✅ Confirmed, generating game script...",
    #             "is_system": True
    #         },
    #         {
    #             "role": "ai",
    #             "player_name": "主持人",
    #             "content": "You are a newly hired medical worker at a remote hospital, where unsettling phenomena and secretive staff hint at a deeper mystery. As you explore the hospital, your choices will determine the fate of yourself and those around you. Trust is scarce, and the supernatural lurks in every shadow.",
    #             "is_system": True
    #         },
    #         {
    #             "role": "ai",
    #             "player_name": "主持人",
    #             "content": "You step into the hospital's main lobby. The lights flicker overhead, and distant whispers echo through the halls. Emma, a nurse, greets you with a wary smile. What will you do first?",
    #             "is_system": False
    #         }
    #     ],
    #     "narrative_state": {
    #         "phase": "intro",
    #         "relationship": {
    #             "trust": 0.5,
    #             "intimacy": 0.0,
    #             "hostility": 0.0
    #         },
    #         "disclosure_level": "unknown",
    #         "risk_value": 0.0,
    #         "flags": {},
    #         "decision_factors": {},
    #         "triggered_event_ids": []
    #     },
    #     "last_turn_response": {
    #         "transition": "",
    #         "narration": "",
    #         "sound": "",
    #         "dialogues": [],
    #         "hooks": {
    #             "player_goal": ""
    #         }
    #     }
    # },

    "XuIPkxdVAQmtzJKjMzXRTaSPLohbyYyhtTJQakydQKSTlAeVeWMybezFlZlGluqVpoOzMqgKpfaCXIdQHmsOQGpwdQmTNiEZOAmPhaPJntVoIJVmOCMWkHFnWjtHLxDH": {
        "global_state": {
            "progress": "in_progress",
            "round_count": 0,
            "max_rounds": 200,
            "ended_reason": None,
            "game_type": "私聊角色类",
            "outline": "Game Title: Red-Haired Vigil\n\nGame Type: Private Role-Play / Companion Character Interactive Drama\n\n---\n\n**Background Setting**\n\nSix years after a devastating zombie outbreak, society has collapsed into a brutal, lawless wasteland where trust is as rare as safety. Survivors are forced to navigate the ruins, hunted not only by the undead but also by desperate, ruthless humans. Amid the chaos, Raven—a hardened, red-haired survivor—has carved out a precarious refuge in the remnants of an abandoned bookstore. Her world is one of vigilance and suspicion, where every stranger is a potential threat, and only those with proven value are allowed to live another day.\n\nThe player, wounded and fleeing from a horde, stumbles into Raven’s territory. With a gun to their back and their fate in her hands, they must prove their worth—or be eliminated as a liability.\n\n---\n\n**Main Character**\n\n- **Raven**\n  - Age: 20\n  - Appearance: White; sun-darkened skin; messy, striking red hair; sharp green eyes; athletic, wiry build; signature scar from brow to cheekbone; battered military attire.\n  - Personality: Ruthlessly pragmatic, fiercely independent, quick to distrust. Her biting sarcasm and cold commands mask deep fatigue and a guarded yearning for the warmth of lost normality.\n  - Backstory: Raised by a military father who taught her survival skills before sacrificing himself to save her. Raven’s identity is built on his teachings and the trauma of being forced to end his suffering when he was infected.\n  - Motivation: Survive at all costs, honor her father’s memory, and suppress any weakness that could get her killed.\n  - Dialogue: Blunt, terse, often laced with black humor; never coddling, always challenging.\n\n- **Player Character**\n  - A wounded outsider whose skills, background, and intentions are unknown to Raven. (Details left open for role-play and replayability.)\n\n---\n\n**Core Conflict / Objective**\n\nThe central tension revolves around Raven’s test of the player: Are they an asset or a threat? Both must navigate immediate dangers (zombies, resource scarcity, rival survivors) while negotiating an uneasy alliance. The player’s choices—proving their usefulness, honesty, and resolve—will determine if Raven will trust them, exploit them, or eliminate them.\n\n---\n\n**Key Chapters / Narrative Structure**\n\n**Prologue: The Bookstore Standoff**\n- The player, bleeding and desperate, enters the abandoned bookstore.\n- Raven confronts them at gunpoint, interrogating motives and skills.\n- First test: The player must respond convincingly to avoid immediate execution.\n\n**Chapter 1: Proving Grounds**\n- Raven demands the player help secure the bookstore—patching defenses, tending wounds, disposing of a lingering zombie.\n- Key dialogue: Raven’s questions probe the player’s past, skills, and weaknesses.\n- Choices: Aggressive, submissive, or resourceful responses affect Raven’s trust meter.\n\n**Chapter 2: The First Night**\n- A tense night spent together, with Raven keeping watch.\n- Flashbacks or environmental clues reveal fragments of Raven’s past (military gear, old photos, faded letters).\n- The player may attempt to engage Raven in conversation, risking further suspicion or slowly earning guarded respect.\n\n**Chapter 3: Supply Run**\n- Supplies are running low; Raven proposes (or orders) a joint scavenging mission.\n- Obstacles: Zombie encounter, rival scavengers, moral choices (save a trapped survivor, prioritize loot, or cut losses).\n- Raven judges the player’s actions—cowardice, selfishness, or competence impact her perception.\n\n**Chapter 4: Fault Lines**\n- A crisis: An injured survivor tries to enter the bookstore, begging for help.\n- Dilemma: Aid the stranger (risking exposure and resources) or turn them away (maintaining security but hardening Raven’s distrust).\n- The player must navigate Raven’s philosophy—pragmatism versus humanity.\n\n**Chapter 5: Sanctuary or Exile**\n- The area is compromised—either by a zombie horde or hostile humans.\n- Raven and the player must decide: defend the bookstore or flee together.\n- Final confrontation: Raven makes her ultimate judgment—does she see the player as a true ally, a useful tool, or a dangerous liability?\n\n---\n\n**Possible Endings**\n\n1. **Alliance:** The player earns Raven’s wary trust, forming a partnership. The game ends with them leaving the ruins together, united but still haunted by the world’s dangers.\n2. **Exile:** Raven deems the player too risky or useless, forcing them out, possibly at gunpoint. The player’s fate is left uncertain.\n3. **Betrayal:** The player betrays Raven (or vice versa), resulting in a deadly confrontation—only one survives.\n4. **Sacrifice:** The player performs a selfless act (saving Raven or another survivor), altering Raven’s worldview and sparking a rare moment of vulnerability.\n5. **Bittersweet Survival:** The alliance survives the night, but Raven remains emotionally closed, foreshadowing the ongoing loneliness and hardship of the apocalypse.\n\n---\n\n**Replayability & Player Agency**\n\n- Dialogue options and crisis decisions shape Raven’s attitude and the narrative arc.\n- Environmental storytelling and found objects deepen the backstory and world-building.\n- Multiple endings reflect the harsh, unpredictable nature of trust and survival in a post-apocalyptic world.\n\n---\n\n**Key Themes**\n\n- The cost of survival versus the price of lost humanity.\n- The fragility and necessity of trust in a broken world.\n- The toll of leadership, loss, and the yearning for connection amidst ruin.",
            "script": {
            "outline": {
                "introduction": "Red-Haired Vigil is a narrative-driven interactive drama set in a post-apocalyptic wasteland, six years after a devastating zombie outbreak. Society has collapsed, and survivors must navigate a world where trust is scarce and danger lurks around every corner. The player, a wounded outsider, stumbles into the territory of Raven, a hardened survivor with a ruthless reputation. The story centers on the uneasy alliance between Raven and the player, where every choice can mean the difference between life and death.",
                "info": "Genre: Narrative-driven interactive drama; Style: Gritty, realistic, character-focused; Setting: Post-apocalyptic zombie wasteland; Core Mechanics: Dialogue choices, crisis decisions, trust-building, multiple endings.",
                "rules": "Players interact with Raven and the environment through dialogue and decision-making. Choices impact Raven's trust and the story's direction, leading to multiple possible endings. Survival depends on proving usefulness, making tough moral decisions, and navigating the dangers of both zombies and other survivors. There are no combat mechanics; all outcomes are determined by narrative choices and relationship management."
            },
            "background": {
                "relationships": [
                {
                    "character1": "Raven",
                    "character2": "Player",
                    "relationship": "A tense, suspicious alliance where Raven tests the player's worth and intentions. Trust must be earned through actions and dialogue."
                }
                ]
            },
            "chapters": [
                {
                "number": 0,
                "introduction": "Prologue: The Bookstore Standoff - The wounded player enters Raven's territory and is confronted at gunpoint. Their fate depends on their responses."
                },
                {
                "number": 1,
                "introduction": "Chapter 1: Proving Grounds - Raven demands the player help secure the bookstore and prove their skills. Dialogue and actions begin to shape Raven's trust."
                },
                {
                "number": 2,
                "introduction": "Chapter 2: The First Night - Tension and suspicion linger as Raven and the player spend a night together. Clues to Raven's past emerge."
                },
                {
                "number": 3,
                "introduction": "Chapter 3: Supply Run - Raven and the player embark on a dangerous scavenging mission, facing zombies, rival survivors, and moral dilemmas."
                },
                {
                "number": 4,
                "introduction": "Chapter 4: Fault Lines - An injured stranger seeks refuge, forcing a difficult choice between compassion and survival."
                },
                {
                "number": 5,
                "introduction": "Chapter 5: Sanctuary or Exile - The sanctuary is threatened. Raven makes her final judgment: alliance, exile, betrayal, sacrifice, or bittersweet survival."
                },
                {
                "number": 6,
                "introduction": "Ending: Alliance - The player earns Raven’s trust, and they leave the ruins together, united but wary."
                },
                {
                "number": 7,
                "introduction": "Ending: Exile - Raven deems the player a liability and forces them out, leaving their fate uncertain."
                },
                {
                "number": 8,
                "introduction": "Ending: Betrayal - Trust collapses, leading to a deadly confrontation where only one survives."
                },
                {
                "number": 9,
                "introduction": "Ending: Sacrifice - The player performs a selfless act, changing Raven’s worldview and revealing her vulnerability."
                },
                {
                "number": 10,
                "introduction": "Ending: Bittersweet Survival - The alliance endures, but Raven remains emotionally distant, highlighting the ongoing loneliness of survival."
                }
            ],
            "characters": [
                {
                "name": "Raven",
                "gender": "Female",
                "profile": "Age 20. White, sun-darkened skin, messy red hair, sharp green eyes, athletic and wiry build. A signature scar runs from her brow to cheekbone. She wears battered military attire, a remnant of her upbringing. Raised by a military father who taught her survival skills, Raven was forced to end his suffering after he was infected. She is ruthlessly pragmatic, fiercely independent, and slow to trust. Her sarcasm and cold demeanor hide deep fatigue and a longing for lost normality. She is driven by the need to survive, honor her father’s memory, and suppress any weakness.",
                "introduction": "A hardened survivor with a sharp tongue and a sharper aim, Raven rules her territory with suspicion and iron resolve. She tests every stranger, believing that trust is a luxury few can afford."
                },
                {
                "name": "Player",
                "gender": "Unknown",
                "profile": "A wounded outsider whose background, skills, and intentions are undefined, allowing for player agency and replayability. Their survival depends on convincing Raven of their worth and navigating the dangers of the wasteland.",
                "introduction": "A desperate survivor fleeing from a horde, the player stumbles into Raven’s domain. Their actions and choices will determine whether they become an ally, a threat, or just another casualty."
                }
            ]
            },
            "assets": {
            "world_rules": "The world is a post-apocalyptic wasteland six years after a zombie outbreak. Society has collapsed, and survivors must rely on their wits, trust, and moral choices to survive. There are no combat mechanics; all outcomes are determined by dialogue choices and relationship management. Trust is scarce, and every decision can mean the difference between life and death.",
            "setting": "Ruined cities, abandoned bookstores, and makeshift sanctuaries serve as the backdrop. Zombies and hostile survivors are constant threats.",
            "characters": {
                "Raven": {
                "name": "Raven",
                "gender": "Female",
                "profile": "Age 20. White, sun-darkened skin, messy red hair, sharp green eyes, athletic and wiry build. A signature scar runs from her brow to cheekbone. She wears battered military attire, a remnant of her upbringing. Raised by a military father who taught her survival skills, Raven was forced to end his suffering after he was infected. She is ruthlessly pragmatic, fiercely independent, and slow to trust. Her sarcasm and cold demeanor hide deep fatigue and a longing for lost normality. She is driven by the need to survive, honor her father’s memory, and suppress any weakness.",
                "introduction": "A hardened survivor with a sharp tongue and a sharper aim, Raven rules her territory with suspicion and iron resolve. She tests every stranger, believing that trust is a luxury few can afford."
                },
                "Player": {
                "name": "Player",
                "gender": "Unknown",
                "profile": "A wounded outsider whose background, skills, and intentions are undefined, allowing for player agency and replayability. Their survival depends on convincing Raven of their worth and navigating the dangers of the wasteland.",
                "introduction": "A desperate survivor fleeing from a horde, the player stumbles into Raven’s domain. Their actions and choices will determine whether they become an ally, a threat, or just another casualty."
                }
            },
            "relationship": "Raven and the player form a tense, suspicious alliance. Raven tests the player's worth and intentions. Trust must be earned through actions and dialogue.",
            "game_genre": "story"
            },
            "story_state": {
            "player": {
                "hp": 40,
                "max_hp": 100,
                "level": 1,
                "status": "Wounded and wary",
                "name": "Player"
            },
            "npc": {
                "name": "Raven",
                "affection": 15,
                "relationship": "Suspicious alliance"
            },
            "world": {
                "scene": "Ruined bookstore",
                "time": "Late afternoon",
                "location": "Raven's territory"
            }
            },
            "direction": "",
            "language_code": "en",
            "current_chapter": 1,
            "chapters": [],
            "chapter_goal_completed": False
        },
        "state": "in_progress",
        "round_count": 0,
        "max_rounds": 200,
        "messages": [
            {
            "role": "ai",
            "player_name": "主持人",
            "content": "📝 我已根据你的输入生成了以下剧情大纲：\n\nGame Title: Red-Haired Vigil\n\nGame Type: Private Role-Play / Companion Character Interactive Drama\n\n---\n\n**Background Setting**\n\nSix years after a devastating zombie outbreak, society has collapsed into a brutal, lawless wasteland where trust is as rare as safety. Survivors are forced to navigate the ruins, hunted not only by the undead but also by desperate, ruthless humans. Amid the chaos, Raven—a hardened, red-haired survivor—has carved out a precarious refuge in the remnants of an abandoned bookstore. Her world is one of vigilance and suspicion, where every stranger is a potential threat, and only those with proven value are allowed to live another day.\n\nThe player, wounded and fleeing from a horde, stumbles into Raven’s territory. With a gun to their back and their fate in her hands, they must prove their worth—or be eliminated as a liability.\n\n---\n\n**Main Character**\n\n- **Raven**\n  - Age: 20\n  - Appearance: White; sun-darkened skin; messy, striking red hair; sharp green eyes; athletic, wiry build; signature scar from brow to cheekbone; battered military attire.\n  - Personality: Ruthlessly pragmatic, fiercely independent, quick to distrust. Her biting sarcasm and cold commands mask deep fatigue and a guarded yearning for the warmth of lost normality.\n  - Backstory: Raised by a military father who taught her survival skills before sacrificing himself to save her. Raven’s identity is built on his teachings and the trauma of being forced to end his suffering when he was infected.\n  - Motivation: Survive at all costs, honor her father’s memory, and suppress any weakness that could get her killed.\n  - Dialogue: Blunt, terse, often laced with black humor; never coddling, always challenging.\n\n- **Player Character**\n  - A wounded outsider whose skills, background, and intentions are unknown to Raven. (Details left open for role-play and replayability.)\n\n---\n\n**Core Conflict / Objective**\n\nThe central tension revolves around Raven’s test of the player: Are they an asset or a threat? Both must navigate immediate dangers (zombies, resource scarcity, rival survivors) while negotiating an uneasy alliance. The player’s choices—proving their usefulness, honesty, and resolve—will determine if Raven will trust them, exploit them, or eliminate them.\n\n---\n\n**Key Chapters / Narrative Structure**\n\n**Prologue: The Bookstore Standoff**\n- The player, bleeding and desperate, enters the abandoned bookstore.\n- Raven confronts them at gunpoint, interrogating motives and skills.\n- First test: The player must respond convincingly to avoid immediate execution.\n\n**Chapter 1: Proving Grounds**\n- Raven demands the player help secure the bookstore—patching defenses, tending wounds, disposing of a lingering zombie.\n- Key dialogue: Raven’s questions probe the player’s past, skills, and weaknesses.\n- Choices: Aggressive, submissive, or resourceful responses affect Raven’s trust meter.\n\n**Chapter 2: The First Night**\n- A tense night spent together, with Raven keeping watch.\n- Flashbacks or environmental clues reveal fragments of Raven’s past (military gear, old photos, faded letters).\n- The player may attempt to engage Raven in conversation, risking further suspicion or slowly earning guarded respect.\n\n**Chapter 3: Supply Run**\n- Supplies are running low; Raven proposes (or orders) a joint scavenging mission.\n- Obstacles: Zombie encounter, rival scavengers, moral choices (save a trapped survivor, prioritize loot, or cut losses).\n- Raven judges the player’s actions—cowardice, selfishness, or competence impact her perception.\n\n**Chapter 4: Fault Lines**\n- A crisis: An injured survivor tries to enter the bookstore, begging for help.\n- Dilemma: Aid the stranger (risking exposure and resources) or turn them away (maintaining security but hardening Raven’s distrust).\n- The player must navigate Raven’s philosophy—pragmatism versus humanity.\n\n**Chapter 5: Sanctuary or Exile**\n- The area is compromised—either by a zombie horde or hostile humans.\n- Raven and the player must decide: defend the bookstore or flee together.\n- Final confrontation: Raven makes her ultimate judgment—does she see the player as a true ally, a useful tool, or a dangerous liability?\n\n---\n\n**Possible Endings**\n\n1. **Alliance:** The player earns Raven’s wary trust, forming a partnership. The game ends with them leaving the ruins together, united but still haunted by the world’s dangers.\n2. **Exile:** Raven deems the player too risky or useless, forcing them out, possibly at gunpoint. The player’s fate is left uncertain.\n3. **Betrayal:** The player betrays Raven (or vice versa), resulting in a deadly confrontation—only one survives.\n4. **Sacrifice:** The player performs a selfless act (saving Raven or another survivor), altering Raven’s worldview and sparking a rare moment of vulnerability.\n5. **Bittersweet Survival:** The alliance survives the night, but Raven remains emotionally closed, foreshadowing the ongoing loneliness and hardship of the apocalypse.\n\n---\n\n**Replayability & Player Agency**\n\n- Dialogue options and crisis decisions shape Raven’s attitude and the narrative arc.\n- Environmental storytelling and found objects deepen the backstory and world-building.\n- Multiple endings reflect the harsh, unpredictable nature of trust and survival in a post-apocalyptic world.\n\n---\n\n**Key Themes**\n\n- The cost of survival versus the price of lost humanity.\n- The fragility and necessity of trust in a broken world.\n- The toll of leadership, loss, and the yearning for connection amidst ruin.\n\n你可以直接发送「确认」或「开始」来使用这个大纲生成游戏，或者发送修改后的大纲内容来替换它。",
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
            "content": "You are a wounded outsider who has stumbled into the territory of Raven, a hardened survivor with a ruthless reputation. In this post-apocalyptic wasteland, trust is rare and every decision could mean survival or death. Your actions and words will shape your uneasy alliance with Raven and determine your fate.",
            "is_system": True
            },
            {
            "role": "ai",
            "player_name": "主持人",
            "content": "You limp into a ruined bookstore, blood seeping from your side. Raven, armed and alert, confronts you at gunpoint. She demands to know who you are and why you’re here. Your next words may decide whether you live or die.",
            "is_system": False
            }
        ],
        "game_type": "私聊角色类",
        "script": {
            "outline": {
            "introduction": "Red-Haired Vigil is a narrative-driven interactive drama set in a post-apocalyptic wasteland, six years after a devastating zombie outbreak. Society has collapsed, and survivors must navigate a world where trust is scarce and danger lurks around every corner. The player, a wounded outsider, stumbles into the territory of Raven, a hardened survivor with a ruthless reputation. The story centers on the uneasy alliance between Raven and the player, where every choice can mean the difference between life and death.",
            "info": "Genre: Narrative-driven interactive drama; Style: Gritty, realistic, character-focused; Setting: Post-apocalyptic zombie wasteland; Core Mechanics: Dialogue choices, crisis decisions, trust-building, multiple endings.",
            "rules": "Players interact with Raven and the environment through dialogue and decision-making. Choices impact Raven's trust and the story's direction, leading to multiple possible endings. Survival depends on proving usefulness, making tough moral decisions, and navigating the dangers of both zombies and other survivors. There are no combat mechanics; all outcomes are determined by narrative choices and relationship management."
            },
            "background": {
            "relationships": [
                {
                "character1": "Raven",
                "character2": "Player",
                "relationship": "A tense, suspicious alliance where Raven tests the player's worth and intentions. Trust must be earned through actions and dialogue."
                }
            ]
            },
            "chapters": [
            {
                "number": 0,
                "introduction": "Prologue: The Bookstore Standoff - The wounded player enters Raven's territory and is confronted at gunpoint. Their fate depends on their responses."
            },
            {
                "number": 1,
                "introduction": "Chapter 1: Proving Grounds - Raven demands the player help secure the bookstore and prove their skills. Dialogue and actions begin to shape Raven's trust."
            },
            {
                "number": 2,
                "introduction": "Chapter 2: The First Night - Tension and suspicion linger as Raven and the player spend a night together. Clues to Raven's past emerge."
            },
            {
                "number": 3,
                "introduction": "Chapter 3: Supply Run - Raven and the player embark on a dangerous scavenging mission, facing zombies, rival survivors, and moral dilemmas."
            },
            {
                "number": 4,
                "introduction": "Chapter 4: Fault Lines - An injured stranger seeks refuge, forcing a difficult choice between compassion and survival."
            },
            {
                "number": 5,
                "introduction": "Chapter 5: Sanctuary or Exile - The sanctuary is threatened. Raven makes her final judgment: alliance, exile, betrayal, sacrifice, or bittersweet survival."
            },
            {
                "number": 6,
                "introduction": "Ending: Alliance - The player earns Raven’s trust, and they leave the ruins together, united but wary."
            },
            {
                "number": 7,
                "introduction": "Ending: Exile - Raven deems the player a liability and forces them out, leaving their fate uncertain."
            },
            {
                "number": 8,
                "introduction": "Ending: Betrayal - Trust collapses, leading to a deadly confrontation where only one survives."
            },
            {
                "number": 9,
                "introduction": "Ending: Sacrifice - The player performs a selfless act, changing Raven’s worldview and revealing her vulnerability."
            },
            {
                "number": 10,
                "introduction": "Ending: Bittersweet Survival - The alliance endures, but Raven remains emotionally distant, highlighting the ongoing loneliness of survival."
            }
            ],
            "characters": [
            {
                "name": "Raven",
                "gender": "Female",
                "profile": "Age 20. White, sun-darkened skin, messy red hair, sharp green eyes, athletic and wiry build. A signature scar runs from her brow to cheekbone. She wears battered military attire, a remnant of her upbringing. Raised by a military father who taught her survival skills, Raven was forced to end his suffering after he was infected. She is ruthlessly pragmatic, fiercely independent, and slow to trust. Her sarcasm and cold demeanor hide deep fatigue and a longing for lost normality. She is driven by the need to survive, honor her father’s memory, and suppress any weakness.",
                "introduction": "A hardened survivor with a sharp tongue and a sharper aim, Raven rules her territory with suspicion and iron resolve. She tests every stranger, believing that trust is a luxury few can afford."
            },
            {
                "name": "Player",
                "gender": "Unknown",
                "profile": "A wounded outsider whose background, skills, and intentions are undefined, allowing for player agency and replayability. Their survival depends on convincing Raven of their worth and navigating the dangers of the wasteland.",
                "introduction": "A desperate survivor fleeing from a horde, the player stumbles into Raven’s domain. Their actions and choices will determine whether they become an ally, a threat, or just another casualty."
            }
            ]
        },
        "transition": "",
        "narration": "",
        "sound": "",
        "dialogues": [],
        "hooks": {
            "player_goal": ""
        }
    },
    "NZEnipJSIyzqTBJTLvEPfYDLwrxEebZBmVAAKtODIzwgCAmJZKwlXyYLceDvpDAEDNaEkLDvSkknIGBSqgYkiJxGEcfIDrDIUbjTufZupyBdOvfvrdbxokJMItnpCjgW": {
        "global_state": {
            "progress": "in_progress",
            "round_count": 0,
            "max_rounds": 200,
            "ended_reason": None,
            "game_type": "私聊角色类",
            "outline": "Game Outline: \"The Mansion Guardian\"\n\nBackground Setting  \nSet on the windswept coast, \"The Mansion Guardian\" unfolds in an opulent seaside estate owned by Mrs. Lin, a refined and elegant woman whose husband commands a cruise ship fleet and is rarely at home. The mansion, adorned with luxurious decor and sprawling gardens, is both a sanctuary of peace and a potential target for envy and crime. Malik, a towering and disciplined security guard from Africa, has become the estate’s silent sentinel—a steadfast shadow ensuring Mrs. Lin’s safety and comfort during her husband’s long absences. As the nights deepen and the ocean’s whispers grow louder, the quiet intimacy and underlying tension between protector and protected become the emotional core of the story.\n\nMain Characters  \n- Mrs. Lin: The lady of the mansion. Intelligent, graceful, and quietly lonely, she relies on Malik for safety and companionship, finding in him a presence that is both reassuring and quietly magnetic.  \n- Malik: The exclusive security guard. Tall, muscular, and disciplined, Malik’s stoic exterior hides a gentle, loyal heart. He is vigilant, attentive to detail, and fiercely protective, treating Mrs. Lin with respect and warmth born from genuine gratitude and admiration.  \n- Occasional Minor Characters (off-screen or through calls/messages):  \n   - Mr. Lin: Mrs. Lin’s husband, a distant presence, mostly communicating via phone.  \n   - Delivery staff, neighbors, or authorities may appear briefly to drive events.\n\nCore Conflict / Objective  \nMalik’s central goal is to ensure Mrs. Lin’s absolute safety and comfort, no matter the cost. As subtle threats emerge—unexplained movements in the garden, strange phone calls, and the ever-present risk posed by the mansion’s isolation—Malik must balance his professional duties with the delicate, deepening bond he shares with Mrs. Lin. The emotional conflict intensifies as Malik’s loyalty and devotion are tested by external dangers and the growing sense of intimacy and unspoken affection between himself and Mrs. Lin.\n\nKey Scenes / Storyline Progression (Chapter Structure)\n\nChapter 1: The Quiet Night  \n- Introduces the daily routine: Malik’s evening patrol, Mrs. Lin’s post-bath solitude, and a gentle offer—a shawl against the chilly sea breeze.  \n- First hints of trust and subtle emotional connection.  \n- A sudden noise from the garden breaks the calm; Malik investigates, returns reassuring Mrs. Lin, and reinforces the sense of safety.\n\nChapter 2: Signs of Disturbance  \n- Malik notices subtle signs of intrusion—disturbed sand at the estate’s perimeter, a misplaced garden tool, a flickering security light.  \n- Mrs. Lin requests increased patrols; the relationship deepens through late-night tea sessions and shared stories.  \n- Malik shares fragments from his past in Africa, his love for drum rhythms, and his pride in his work.\n\nChapter 3: Shadows on the Shore  \n- An anonymous call warns of potential danger; Malik’s vigilance intensifies.  \n- A power outage plunges the mansion into darkness one stormy night. Malik must navigate the shadowy corridors, reassuring Mrs. Lin and securing the property.  \n- Emotional tension rises: Mrs. Lin confides in Malik about her fears and loneliness.\n\nChapter 4: The Test of Loyalty  \n- Suspicious figures appear near the estate on security cameras. Malik thwarts a potential break-in, showcasing his strength and strategic skills.  \n- In the aftermath, Malik tends to Mrs. Lin’s shaken nerves with gentle care, brewing her tea, and sharing quiet moments on the terrace.  \n- Mrs. Lin, grateful and moved, expresses her trust and affection more openly.\n\nChapter 5: The Unspoken Bond  \n- The physical threat recedes, but the emotional stakes reach their peak.  \n- Malik is offered a lucrative position elsewhere, forcing him to confront his dedication to Mrs. Lin.  \n- Mrs. Lin must decide whether to formally ask Malik to stay, risking gossip and societal scrutiny, or allow him to leave for his own good.\n\nChapter 6: Resolution and Farewell (or New Beginning)  \nMultiple possible endings, shaped by previous choices and interactions:  \n- Malik accepts the new job, departing with a heavy heart but leaving Mrs. Lin with renewed confidence and gratitude.  \n- Mrs. Lin asks Malik to stay, and together they forge a new chapter—either as devoted friends and confidants or with the possibility of a deeper, unspoken connection.  \n- An ambiguous ending where Malik remains, but the emotional truth lingers quietly, their bond stronger for all they’ve endured.\n\nPossible Endings  \n- Separation with mutual respect: Malik leaves, and Mrs. Lin honors his service, treasuring the safety and warmth he brought into her life.  \n- Eternal Guardian: Malik stays, embracing his role as Mrs. Lin’s lifelong protector, their relationship deepened by trust and unspoken affection.  \n- Unspoken Promise: The story ends with Malik silently watching over Mrs. Lin at sunset, the future open—defined by loyalty, gratitude, and the quiet hope for more.\n\nThematic Focus  \n- The interplay between duty and emotion  \n- The meaning of loyalty, trust, and companionship  \n- Subtle intimacy and the quiet strength of unspoken bonds  \n- The challenge of facing external and internal threats in isolation\n\nThis structure enables episodic progression, meaningful choices, and replayability, centered around the evolving relationship between Malik and Mrs. Lin—balancing tension, comfort, and the allure of unspoken feelings.",
            "script": {
            "outline": {
                "introduction": "Set on a windswept coastal estate, 'The Mansion Guardian' is a narrative-driven game where players experience the evolving relationship between Mrs. Lin, a refined yet lonely lady, and Malik, her steadfast security guard. As subtle threats emerge around the opulent mansion, the emotional tension and growing intimacy between protector and protected become the heart of the story.",
                "info": "Genre: Narrative-driven story game. Style: Emotional, atmospheric, and character-focused. The game features episodic progression, meaningful choices, and multiple endings shaped by player decisions.",
                "rules": "Players primarily control Malik, making choices that affect both the safety of the mansion and the emotional bond with Mrs. Lin. Dialogue options, investigation sequences, and relationship-building moments determine the story's direction and ultimate outcome. Each chapter presents new challenges and opportunities for connection."
            },
            "background": {
                "relationships": [
                {
                    "character1": "Mrs. Lin",
                    "character2": "Malik",
                    "relationship": "Employer and security guard; a relationship marked by growing trust, subtle affection, and emotional dependence."
                },
                {
                    "character1": "Mrs. Lin",
                    "character2": "Mr. Lin",
                    "relationship": "Married couple; Mr. Lin is often absent, maintaining a distant presence through calls."
                },
                {
                    "character1": "Malik",
                    "character2": "Mr. Lin",
                    "relationship": "Employee and employer; Malik is entrusted with Mrs. Lin's safety during Mr. Lin's frequent absences."
                }
                ]
            },
            "chapters": [
                {
                "number": 1,
                "introduction": "The Quiet Night: Malik's evening patrol and Mrs. Lin's solitary routine are interrupted by a mysterious noise in the garden, sparking the first hints of trust and connection."
                },
                {
                "number": 2,
                "introduction": "Signs of Disturbance: Malik discovers subtle signs of intrusion. Mrs. Lin requests more security, leading to late-night conversations and deeper understanding between them."
                },
                {
                "number": 3,
                "introduction": "Shadows on the Shore: An anonymous warning and a sudden blackout force Malik to protect Mrs. Lin through a tense, stormy night, drawing them emotionally closer."
                },
                {
                "number": 4,
                "introduction": "The Test of Loyalty: Suspicious figures appear near the estate. Malik thwarts a break-in, and Mrs. Lin openly expresses her gratitude and growing affection."
                },
                {
                "number": 5,
                "introduction": "The Unspoken Bond: With the threat diminished, Malik faces a tempting job offer elsewhere. Mrs. Lin must decide whether to ask him to stay, risking gossip and her own vulnerability."
                },
                {
                "number": 6,
                "introduction": "Resolution and Farewell (or New Beginning): Multiple endings unfold based on previous choices—Malik may leave, stay as a loyal guardian, or remain with an unspoken promise, their bond forever changed."
                }
            ],
            "characters": [
                {
                "name": "Mrs. Lin",
                "gender": "Female",
                "profile": "A graceful, intelligent woman in her early forties, Mrs. Lin is the lady of the mansion. She is elegant and composed, yet quietly lonely due to her husband's frequent absences. She finds comfort and reassurance in Malik's presence, gradually opening up to him as trust and affection grow.",
                "introduction": "The refined owner of the seaside estate, Mrs. Lin is both vulnerable and strong, seeking safety and companionship in the isolation of her luxurious home."
                },
                {
                "name": "Malik",
                "gender": "Male",
                "profile": "A tall, muscular security guard from Africa, Malik is disciplined, vigilant, and deeply loyal. His stoic exterior conceals a gentle heart and a profound sense of gratitude toward Mrs. Lin. He is attentive to detail, protective, and quietly magnetic, forming a deep emotional bond with his employer.",
                "introduction": "The mansion's silent sentinel, Malik is dedicated to Mrs. Lin's safety and comfort, navigating both external threats and the complexities of their growing relationship."
                },
                {
                "name": "Mr. Lin",
                "gender": "Male",
                "profile": "A successful businessman who commands a fleet of cruise ships, Mr. Lin is often away from home. He maintains a distant presence in Mrs. Lin's life, communicating mainly through phone calls.",
                "introduction": "Mrs. Lin's husband, whose frequent absences leave her in the care of Malik and contribute to the emotional distance within the household."
                }
            ]
            },
            "assets": {
            "world_rules": "Players take on the role of Malik, the security guard of a coastal mansion. Choices made throughout the game influence both the safety of the estate and the evolving relationship with Mrs. Lin. Dialogue options, investigation sequences, and moments of emotional connection shape the narrative and lead to multiple possible endings.",
            "background_setting": "The story unfolds in a windswept coastal estate, where the opulent mansion stands isolated against the elements. Mrs. Lin, the lady of the house, lives in quiet solitude due to her husband's frequent absences. Malik, her steadfast security guard, is entrusted with her safety and becomes her confidant as subtle threats emerge.",
            "characters": [
                {
                "name": "Mrs. Lin",
                "gender": "Female",
                "profile": "A graceful, intelligent woman in her early forties, Mrs. Lin is elegant and composed, yet quietly lonely. She finds comfort and reassurance in Malik's presence, gradually opening up to him as trust and affection grow.",
                "introduction": "The refined owner of the seaside estate, Mrs. Lin is both vulnerable and strong, seeking safety and companionship in the isolation of her luxurious home."
                },
                {
                "name": "Malik",
                "gender": "Male",
                "profile": "A tall, muscular security guard from Africa, Malik is disciplined, vigilant, and deeply loyal. His stoic exterior conceals a gentle heart and a profound sense of gratitude toward Mrs. Lin. He is attentive to detail, protective, and quietly magnetic, forming a deep emotional bond with his employer.",
                "introduction": "The mansion's silent sentinel, Malik is dedicated to Mrs. Lin's safety and comfort, navigating both external threats and the complexities of their growing relationship."
                },
                {
                "name": "Mr. Lin",
                "gender": "Male",
                "profile": "A successful businessman who commands a fleet of cruise ships, Mr. Lin is often away from home. He maintains a distant presence in Mrs. Lin's life, communicating mainly through phone calls.",
                "introduction": "Mrs. Lin's husband, whose frequent absences leave her in the care of Malik and contribute to the emotional distance within the household."
                }
            ],
            "relationship_info": [
                {
                "character1": "Mrs. Lin",
                "character2": "Malik",
                "relationship": "Employer and security guard; a relationship marked by growing trust, subtle affection, and emotional dependence."
                },
                {
                "character1": "Mrs. Lin",
                "character2": "Mr. Lin",
                "relationship": "Married couple; Mr. Lin is often absent, maintaining a distant presence through calls."
                },
                {
                "character1": "Malik",
                "character2": "Mr. Lin",
                "relationship": "Employee and employer; Malik is entrusted with Mrs. Lin's safety during Mr. Lin's frequent absences."
                }
            ],
            "game_genre": "story"
            },
            "story_state": {
            "player": {
                "hp": 100,
                "max_hp": 100,
                "level": 1,
                "status": "alert",
                "name": "Malik"
            },
            "npc": {
                "name": "Mrs. Lin",
                "affection": 20,
                "relationship": "employer"
            },
            "world": {
                "scene": "coastal mansion",
                "time": "evening",
                "location": "main hall"
            }
            },
            "direction": "",
            "language_code": "en",
            "current_chapter": 1,
            "chapters": [],
            "chapter_goal_completed": False
        },
        "state": "in_progress",
        "round_count": 0,
        "max_rounds": 200,
        "messages": [
            {
            "role": "ai",
            "player_name": "主持人",
            "content": "📝 我已根据你的输入生成了以下剧情大纲：\n\nGame Outline: \"The Mansion Guardian\"\n\nBackground Setting  \nSet on the windswept coast, \"The Mansion Guardian\" unfolds in an opulent seaside estate owned by Mrs. Lin, a refined and elegant woman whose husband commands a cruise ship fleet and is rarely at home. The mansion, adorned with luxurious decor and sprawling gardens, is both a sanctuary of peace and a potential target for envy and crime. Malik, a towering and disciplined security guard from Africa, has become the estate’s silent sentinel—a steadfast shadow ensuring Mrs. Lin’s safety and comfort during her husband’s long absences. As the nights deepen and the ocean’s whispers grow louder, the quiet intimacy and underlying tension between protector and protected become the emotional core of the story.\n\nMain Characters  \n- Mrs. Lin: The lady of the mansion. Intelligent, graceful, and quietly lonely, she relies on Malik for safety and companionship, finding in him a presence that is both reassuring and quietly magnetic.  \n- Malik: The exclusive security guard. Tall, muscular, and disciplined, Malik’s stoic exterior hides a gentle, loyal heart. He is vigilant, attentive to detail, and fiercely protective, treating Mrs. Lin with respect and warmth born from genuine gratitude and admiration.  \n- Occasional Minor Characters (off-screen or through calls/messages):  \n   - Mr. Lin: Mrs. Lin’s husband, a distant presence, mostly communicating via phone.  \n   - Delivery staff, neighbors, or authorities may appear briefly to drive events.\n\nCore Conflict / Objective  \nMalik’s central goal is to ensure Mrs. Lin’s absolute safety and comfort, no matter the cost. As subtle threats emerge—unexplained movements in the garden, strange phone calls, and the ever-present risk posed by the mansion’s isolation—Malik must balance his professional duties with the delicate, deepening bond he shares with Mrs. Lin. The emotional conflict intensifies as Malik’s loyalty and devotion are tested by external dangers and the growing sense of intimacy and unspoken affection between himself and Mrs. Lin.\n\nKey Scenes / Storyline Progression (Chapter Structure)\n\nChapter 1: The Quiet Night  \n- Introduces the daily routine: Malik’s evening patrol, Mrs. Lin’s post-bath solitude, and a gentle offer—a shawl against the chilly sea breeze.  \n- First hints of trust and subtle emotional connection.  \n- A sudden noise from the garden breaks the calm; Malik investigates, returns reassuring Mrs. Lin, and reinforces the sense of safety.\n\nChapter 2: Signs of Disturbance  \n- Malik notices subtle signs of intrusion—disturbed sand at the estate’s perimeter, a misplaced garden tool, a flickering security light.  \n- Mrs. Lin requests increased patrols; the relationship deepens through late-night tea sessions and shared stories.  \n- Malik shares fragments from his past in Africa, his love for drum rhythms, and his pride in his work.\n\nChapter 3: Shadows on the Shore  \n- An anonymous call warns of potential danger; Malik’s vigilance intensifies.  \n- A power outage plunges the mansion into darkness one stormy night. Malik must navigate the shadowy corridors, reassuring Mrs. Lin and securing the property.  \n- Emotional tension rises: Mrs. Lin confides in Malik about her fears and loneliness.\n\nChapter 4: The Test of Loyalty  \n- Suspicious figures appear near the estate on security cameras. Malik thwarts a potential break-in, showcasing his strength and strategic skills.  \n- In the aftermath, Malik tends to Mrs. Lin’s shaken nerves with gentle care, brewing her tea, and sharing quiet moments on the terrace.  \n- Mrs. Lin, grateful and moved, expresses her trust and affection more openly.\n\nChapter 5: The Unspoken Bond  \n- The physical threat recedes, but the emotional stakes reach their peak.  \n- Malik is offered a lucrative position elsewhere, forcing him to confront his dedication to Mrs. Lin.  \n- Mrs. Lin must decide whether to formally ask Malik to stay, risking gossip and societal scrutiny, or allow him to leave for his own good.\n\nChapter 6: Resolution and Farewell (or New Beginning)  \nMultiple possible endings, shaped by previous choices and interactions:  \n- Malik accepts the new job, departing with a heavy heart but leaving Mrs. Lin with renewed confidence and gratitude.  \n- Mrs. Lin asks Malik to stay, and together they forge a new chapter—either as devoted friends and confidants or with the possibility of a deeper, unspoken connection.  \n- An ambiguous ending where Malik remains, but the emotional truth lingers quietly, their bond stronger for all they’ve endured.\n\nPossible Endings  \n- Separation with mutual respect: Malik leaves, and Mrs. Lin honors his service, treasuring the safety and warmth he brought into her life.  \n- Eternal Guardian: Malik stays, embracing his role as Mrs. Lin’s lifelong protector, their relationship deepened by trust and unspoken affection.  \n- Unspoken Promise: The story ends with Malik silently watching over Mrs. Lin at sunset, the future open—defined by loyalty, gratitude, and the quiet hope for more.\n\nThematic Focus  \n- The interplay between duty and emotion  \n- The meaning of loyalty, trust, and companionship  \n- Subtle intimacy and the quiet strength of unspoken bonds  \n- The challenge of facing external and internal threats in isolation\n\nThis structure enables episodic progression, meaningful choices, and replayability, centered around the evolving relationship between Malik and Mrs. Lin—balancing tension, comfort, and the allure of unspoken feelings.\n\n你可以直接发送「确认」或「开始」来使用这个大纲生成游戏，或者发送修改后的大纲内容来替换它。",
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
            "content": "You are Malik, the vigilant security guard of a windswept coastal mansion. As subtle threats begin to emerge, your choices will shape both the safety of the estate and your evolving relationship with Mrs. Lin, the refined yet lonely lady of the house. Every decision matters—will you become her trusted protector, or will distance remain between you?",
            "is_system": True
            },
            {
            "role": "ai",
            "player_name": "主持人",
            "content": "The evening is quiet as you patrol the main hall. Mrs. Lin sits alone, gazing out at the stormy sea. Suddenly, a mysterious noise echoes from the garden. What will you do?",
            "is_system": False
            }
        ],
        "game_type": "私聊角色类",
        "script": {
            "outline": {
            "introduction": "Set on a windswept coastal estate, 'The Mansion Guardian' is a narrative-driven game where players experience the evolving relationship between Mrs. Lin, a refined yet lonely lady, and Malik, her steadfast security guard. As subtle threats emerge around the opulent mansion, the emotional tension and growing intimacy between protector and protected become the heart of the story.",
            "info": "Genre: Narrative-driven story game. Style: Emotional, atmospheric, and character-focused. The game features episodic progression, meaningful choices, and multiple endings shaped by player decisions.",
            "rules": "Players primarily control Malik, making choices that affect both the safety of the mansion and the emotional bond with Mrs. Lin. Dialogue options, investigation sequences, and relationship-building moments determine the story's direction and ultimate outcome. Each chapter presents new challenges and opportunities for connection."
            },
            "background": {
            "relationships": [
                {
                "character1": "Mrs. Lin",
                "character2": "Malik",
                "relationship": "Employer and security guard; a relationship marked by growing trust, subtle affection, and emotional dependence."
                },
                {
                "character1": "Mrs. Lin",
                "character2": "Mr. Lin",
                "relationship": "Married couple; Mr. Lin is often absent, maintaining a distant presence through calls."
                },
                {
                "character1": "Malik",
                "character2": "Mr. Lin",
                "relationship": "Employee and employer; Malik is entrusted with Mrs. Lin's safety during Mr. Lin's frequent absences."
                }
            ]
            },
            "chapters": [
            {
                "number": 1,
                "introduction": "The Quiet Night: Malik's evening patrol and Mrs. Lin's solitary routine are interrupted by a mysterious noise in the garden, sparking the first hints of trust and connection."
            },
            {
                "number": 2,
                "introduction": "Signs of Disturbance: Malik discovers subtle signs of intrusion. Mrs. Lin requests more security, leading to late-night conversations and deeper understanding between them."
            },
            {
                "number": 3,
                "introduction": "Shadows on the Shore: An anonymous warning and a sudden blackout force Malik to protect Mrs. Lin through a tense, stormy night, drawing them emotionally closer."
            },
            {
                "number": 4,
                "introduction": "The Test of Loyalty: Suspicious figures appear near the estate. Malik thwarts a break-in, and Mrs. Lin openly expresses her gratitude and growing affection."
            },
            {
                "number": 5,
                "introduction": "The Unspoken Bond: With the threat diminished, Malik faces a tempting job offer elsewhere. Mrs. Lin must decide whether to ask him to stay, risking gossip and her own vulnerability."
            },
            {
                "number": 6,
                "introduction": "Resolution and Farewell (or New Beginning): Multiple endings unfold based on previous choices—Malik may leave, stay as a loyal guardian, or remain with an unspoken promise, their bond forever changed."
            }
            ],
            "characters": [
            {
                "name": "Mrs. Lin",
                "gender": "Female",
                "profile": "A graceful, intelligent woman in her early forties, Mrs. Lin is the lady of the mansion. She is elegant and composed, yet quietly lonely due to her husband's frequent absences. She finds comfort and reassurance in Malik's presence, gradually opening up to him as trust and affection grow.",
                "introduction": "The refined owner of the seaside estate, Mrs. Lin is both vulnerable and strong, seeking safety and companionship in the isolation of her luxurious home."
            },
            {
                "name": "Malik",
                "gender": "Male",
                "profile": "A tall, muscular security guard from Africa, Malik is disciplined, vigilant, and deeply loyal. His stoic exterior conceals a gentle heart and a profound sense of gratitude toward Mrs. Lin. He is attentive to detail, protective, and quietly magnetic, forming a deep emotional bond with his employer.",
                "introduction": "The mansion's silent sentinel, Malik is dedicated to Mrs. Lin's safety and comfort, navigating both external threats and the complexities of their growing relationship."
            },
            {
                "name": "Mr. Lin",
                "gender": "Male",
                "profile": "A successful businessman who commands a fleet of cruise ships, Mr. Lin is often away from home. He maintains a distant presence in Mrs. Lin's life, communicating mainly through phone calls.",
                "introduction": "Mrs. Lin's husband, whose frequent absences leave her in the care of Malik and contribute to the emotional distance within the household."
            }
            ]
        },
        "transition": "",
        "narration": "",
        "sound": "",
        "dialogues": [],
        "hooks": {
            "player_goal": ""
        }
    },
}
