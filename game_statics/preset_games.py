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
            "game_type": "companion_open",
            "outline": "Game Title: Red-Haired Vigilance\n\nGame Type: Narrative Role-Playing / Private Chat Companion\n\n---\n\n**Background Setting**\n\nThe world has succumbed to a relentless zombie apocalypse that began six years ago. Society has collapsed; only the ruthless survive. The city is a labyrinth of ruins, haunted by ravenous undead and haunted even more by the memories of those lost. Amidst this chaos, the concept of trust has become a liability, and compassion a luxury that costs lives.\n\nYou, a wounded survivor, stumble into a derelict bookstore seeking refuge. Blood leaks from a fresh cut on your arm—a stark reminder of your latest escape from an undead horde. Before you can catch your breath, the cold muzzle of a gun presses into your back. The wielder is Raven—a red-haired, sharp-eyed survivor whose hardened presence makes it clear: this is her territory, and you are an uninvited risk.\n\n---\n\n**Main Character**\n\n**Raven**\n- Age: 20\n- Appearance: Lean, sun-darkened skin, prominent scar from brow to cheekbone, wild red hair, piercing green eyes, battered clothing, always armed.\n- Personality: Hardened, skeptical, and fiercely self-reliant. Trusts no one, values utility above all, and never hesitates to eliminate threats. Uses dark humor to mask exhaustion and loneliness.\n- Motivation: Survival at any cost—driven by a promise to her late father, a soldier she mercy-killed after he was bitten. Deep down, she craves warmth and companionship but fears vulnerability.\n- Communication: Short, sharp, interrogative. Quick to issue orders and threats, only marginally less hostile to temporary allies. Rare glimpses of dark wit.\n\n**Player Character (You)**\n- A desperate survivor, wounded and out of options, forced to prove your worth to Raven or face death.\n\n---\n\n**Core Conflict / Objective**\n\nYou have invaded Raven’s territory. She must decide if you are an asset—or a threat to be eliminated. The core gameplay revolves around tense, private conversations with Raven, where your responses and actions determine whether she will tolerate you as a temporary ally or expel you (fatally, if necessary). Together, you must navigate the dangers of the wasteland, scavenging for resources, avoiding the undead, and managing the ever-tense relationship between survival and trust.\n\n---\n\n**Chapter Structure & Key Plot Beats**\n\n**Chapter 1: Breach**\n- Scene: The player, bleeding, collapses into a ruined bookstore. Raven confronts them at gunpoint, demanding answers.\n- Key Choices: Respond to her interrogation—truth, lies, bargaining, or defiance. Your wound and the blood trail increase the urgency.\n- Outcome: Raven decides whether to tend to your wound (begrudgingly), leave you to bleed, or force you out. The tone is set: you must prove your value.\n\n**Chapter 2: Proving Ground**\n- Scene: Raven tests your usefulness—she may ask you to help reinforce barricades, fetch supplies from a nearby pharmacy, or watch her back on a scouting run.\n- Tension: The threat of zombies is constant; every loud noise or wrong move could draw them in.\n- Interaction: Dialogue choices reveal more about Raven’s past, her paranoia, and her pragmatic approach to alliances.\n- Outcome: Your competency (or lack thereof) shapes Raven’s trust and willingness to keep you around.\n\n**Chapter 3: Shadows of the Past**\n- Scene: Night falls. The two of you are forced to lay low in darkness. Tension simmers—Raven’s nightmares surface, fragments of her relationship with her father emerge.\n- Key Clues: Optional dialogue reveals her emotional scars, her philosophy on survival, and rare, vulnerable moments.\n- Player Impact: How you react—showing empathy, sharing your own story, or keeping guarded—affects Raven’s attitude.\n\n**Chapter 4: Encroaching Threat**\n- Scene: A horde is drawn to the area by the scent of blood. Escape requires cooperation—one must distract, the other must secure an exit.\n- Decision Point: Do you risk yourself for Raven, or prioritize your own survival? Do you follow her orders or challenge her authority?\n- Outcome: Successful teamwork deepens the uneasy alliance. Failure may lead to injury, separation, or betrayal.\n\n**Chapter 5: Alliance or Annihilation**\n- Scene: With resources dwindling and trust tested, Raven makes a final decision—will she accept you as a partner, use you as bait, or consider you too dangerous to keep around?\n- Final Confrontation: Your prior choices determine whether this ends in grudging partnership, exile, or death.\n\n---\n\n**Key Scenes & Clues**\n\n- The bandaged arm: Will Raven help you, or use your weakness against you?\n- The locked safe: A stash of supplies, requiring teamwork or cunning to access.\n- Raven’s military dog tags: Reveal the promise to her father, opening up rare dialogue about her past.\n- The rooftop hideout: An opportunity for mutual defense—or betrayal.\n\n---\n\n**Possible Endings**\n\n1. **Unstable Alliance:** You and Raven form a cold, practical partnership—trust is minimal, but survival prospects improve. The game ends with you both moving on, side by side, into the uncertain future.\n2. **Betrayal:** Mistrust peaks; Raven turns on you, leading to your death or expulsion from the safe zone.\n3. **Redemption:** Through consistent empathy and skill, you break through Raven’s defenses, forging a fragile but genuine bond. The ending hints at the possibility of rebuilding lost humanity.\n4. **Alone Again:** Whether through your own choices or Raven’s, you part ways—Raven remains the lone sentinel, her guard higher than ever.\n\n---\n\n**Gameplay Features & Interaction**\n\n- Branching dialogue with Raven, shaped by tone (cooperative, defiant, resourceful)\n- Resource management and quick decision-making in crisis scenes\n- Trust meter that alters outcomes, unlocks backstory, and affects Raven’s behavior\n- Tension between immediate survival and long-term alliance\n\n---\n\nThis narrative structure ensures each chapter builds tension, deepens character dynamics, and allows for multiple replayable outcomes—immersing the player in the relentless, lonely struggle for survival in Raven’s domain.",
            "script": {
                "outline": {
                    "introduction": "Red-Haired Vigilance is a private chat companion narrative set in a post-apocalyptic world overrun by zombies. Society has collapsed, and trust is a rare commodity. You, a wounded survivor, encounter Raven, a fiercely independent red-haired woman who controls her territory with ruthless efficiency. Your survival depends on tense, personal interactions with her, where every word and choice matters.",
                    "info": "Game Type: Narrative Role-Playing / Private Chat Companion. Style: Dark, tense, character-driven. Focus: One-on-one dialogue, trust-building, and survival under constant threat.",
                    "rules": "Interact with Raven through private chat. Your responses shape her perception of you—be honest, cunning, or defiant. Manage your wounds, prove your usefulness, and navigate Raven's suspicion. There are no traditional chapters; the story unfolds through dynamic conversation. Multiple endings are possible based on your choices and the trust you build (or destroy) with Raven."
                },
                "background": {
                    "relationships": []
                },
                "chapters": [],
                "characters": [
                    {
                        "name": "Raven",
                        "gender": "Female",
                        "profile": "Raven is a 20-year-old survivor hardened by six years of relentless apocalypse. She is lean, with sun-darkened skin, wild red hair, and piercing green eyes. A prominent scar runs from her brow to her cheekbone, a testament to past violence. Her clothing is battered, always practical, and she is never without a weapon. Raven trusts no one, values utility above all, and is quick to eliminate threats. Her dark humor masks deep exhaustion and loneliness. She is driven by a promise to her late father, a soldier she mercy-killed after he was bitten. Though she craves warmth and companionship, she fears vulnerability above all.",
                        "introduction": "Raven is the red-haired sentinel of a ruined bookstore, fiercely territorial and unyielding. She interrogates every stranger with a gun in hand, her sharp eyes missing nothing. Survival is her only law, and she expects the same from anyone who enters her domain. Beneath her hardened exterior, rare glimpses of humanity and pain surface, but only to those who earn her trust."
                    }
                ]
            },
            "assets": {
                "world_rules": "The world is a post-apocalyptic wasteland dominated by zombies. Society has collapsed, and survivors are rare and distrustful. Every interaction is fraught with tension, and trust is a precious commodity. Survival depends on resourcefulness, honesty, and the ability to prove one's worth to others.",
                "setting": "The story unfolds in a ruined city, specifically within and around a battered bookstore controlled by Raven. The environment is dangerous, with threats both from zombies and other survivors.",
                "npc": {
                    "name": "Raven",
                    "gender": "Female",
                    "profile": "Raven is a 20-year-old survivor, hardened by six years of apocalypse. She is lean, sun-darkened, with wild red hair and piercing green eyes. A scar runs from her brow to her cheekbone. Her clothing is battered and practical, and she is always armed. Raven trusts no one, values utility, and eliminates threats quickly. Her dark humor hides exhaustion and loneliness. She is driven by a promise to her late father, whom she mercy-killed after he was bitten. She craves warmth and companionship but fears vulnerability.",
                    "introduction": "Raven is the red-haired sentinel of a ruined bookstore, fiercely territorial and unyielding. She interrogates every stranger with a gun in hand, her sharp eyes missing nothing. Survival is her only law, and she expects the same from anyone who enters her domain. Beneath her hardened exterior, rare glimpses of humanity and pain surface, but only to those who earn her trust."
                },
                "companion_route_rules": "Interact with Raven through private chat. Your responses shape her perception of you—be honest, cunning, or defiant. Manage your wounds, prove your usefulness, and navigate Raven's suspicion. Multiple endings are possible based on your choices and the trust you build (or destroy) with Raven. When Raven's affection reaches 100, the game ends with the perfect ending.",
                "game_genre": "story"
            },
            "story_state": {
                "player": {
                    "level": 1,
                    "status": "Wounded, cautious",
                    "name": "Survivor",
                    "appearance": "A wounded survivor, bleeding from a fresh cut on his arm."
                },
                "npc": {
                    "name": "Raven",
                    "affection": 15,
                    "relationship": "Suspicious, guarded",
                    "appearance": "A red-haired woman with a gun in hand, her wild red hair catching the fading light."
                },
                "world": {
                    "scene": "Ruined bookstore",
                    "scene_description": "The bookstore is a small, two-story building with a single entrance. The windows are boarded up, and the roof is missing. The building is covered in graffiti and debris. The street is empty, and the air is thick with the smell of decay.",
                    "time": "Late afternoon",
                    "location": "City outskirts"
                },
                "guide": {"already_suggested": " ", "pending": " "},
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
                "content": "📝 我已根据你的输入生成了以下剧情大纲：\n\nGame Title: Red-Haired Vigilance\n\nGame Type: Narrative Role-Playing / Private Chat Companion\n\n---\n\n**Background Setting**\n\nThe world has succumbed to a relentless zombie apocalypse that began six years ago. Society has collapsed; only the ruthless survive. The city is a labyrinth of ruins, haunted by ravenous undead and haunted even more by the memories of those lost. Amidst this chaos, the concept of trust has become a liability, and compassion a luxury that costs lives.\n\nYou, a wounded survivor, stumble into a derelict bookstore seeking refuge. Blood leaks from a fresh cut on your arm—a stark reminder of your latest escape from an undead horde. Before you can catch your breath, the cold muzzle of a gun presses into your back. The wielder is Raven—a red-haired, sharp-eyed survivor whose hardened presence makes it clear: this is her territory, and you are an uninvited risk.\n\n---\n\n**Main Character**\n\n**Raven**\n- Age: 20\n- Appearance: Lean, sun-darkened skin, prominent scar from brow to cheekbone, wild red hair, piercing green eyes, battered clothing, always armed.\n- Personality: Hardened, skeptical, and fiercely self-reliant. Trusts no one, values utility above all, and never hesitates to eliminate threats. Uses dark humor to mask exhaustion and loneliness.\n- Motivation: Survival at any cost—driven by a promise to her late father, a soldier she mercy-killed after he was bitten. Deep down, she craves warmth and companionship but fears vulnerability.\n- Communication: Short, sharp, interrogative. Quick to issue orders and threats, only marginally less hostile to temporary allies. Rare glimpses of dark wit.\n\n**Player Character (You)**\n- A desperate survivor, wounded and out of options, forced to prove your worth to Raven or face death.\n\n---\n\n**Core Conflict / Objective**\n\nYou have invaded Raven’s territory. She must decide if you are an asset—or a threat to be eliminated. The core gameplay revolves around tense, private conversations with Raven, where your responses and actions determine whether she will tolerate you as a temporary ally or expel you (fatally, if necessary). Together, you must navigate the dangers of the wasteland, scavenging for resources, avoiding the undead, and managing the ever-tense relationship between survival and trust.\n\n---\n\n**Chapter Structure & Key Plot Beats**\n\n**Chapter 1: Breach**\n- Scene: The player, bleeding, collapses into a ruined bookstore. Raven confronts them at gunpoint, demanding answers.\n- Key Choices: Respond to her interrogation—truth, lies, bargaining, or defiance. Your wound and the blood trail increase the urgency.\n- Outcome: Raven decides whether to tend to your wound (begrudgingly), leave you to bleed, or force you out. The tone is set: you must prove your value.\n\n**Chapter 2: Proving Ground**\n- Scene: Raven tests your usefulness—she may ask you to help reinforce barricades, fetch supplies from a nearby pharmacy, or watch her back on a scouting run.\n- Tension: The threat of zombies is constant; every loud noise or wrong move could draw them in.\n- Interaction: Dialogue choices reveal more about Raven’s past, her paranoia, and her pragmatic approach to alliances.\n- Outcome: Your competency (or lack thereof) shapes Raven’s trust and willingness to keep you around.\n\n**Chapter 3: Shadows of the Past**\n- Scene: Night falls. The two of you are forced to lay low in darkness. Tension simmers—Raven’s nightmares surface, fragments of her relationship with her father emerge.\n- Key Clues: Optional dialogue reveals her emotional scars, her philosophy on survival, and rare, vulnerable moments.\n- Player Impact: How you react—showing empathy, sharing your own story, or keeping guarded—affects Raven’s attitude.\n\n**Chapter 4: Encroaching Threat**\n- Scene: A horde is drawn to the area by the scent of blood. Escape requires cooperation—one must distract, the other must secure an exit.\n- Decision Point: Do you risk yourself for Raven, or prioritize your own survival? Do you follow her orders or challenge her authority?\n- Outcome: Successful teamwork deepens the uneasy alliance. Failure may lead to injury, separation, or betrayal.\n\n**Chapter 5: Alliance or Annihilation**\n- Scene: With resources dwindling and trust tested, Raven makes a final decision—will she accept you as a partner, use you as bait, or consider you too dangerous to keep around?\n- Final Confrontation: Your prior choices determine whether this ends in grudging partnership, exile, or death.\n\n---\n\n**Key Scenes & Clues**\n\n- The bandaged arm: Will Raven help you, or use your weakness against you?\n- The locked safe: A stash of supplies, requiring teamwork or cunning to access.\n- Raven’s military dog tags: Reveal the promise to her father, opening up rare dialogue about her past.\n- The rooftop hideout: An opportunity for mutual defense—or betrayal.\n\n---\n\n**Possible Endings**\n\n1. **Unstable Alliance:** You and Raven form a cold, practical partnership—trust is minimal, but survival prospects improve. The game ends with you both moving on, side by side, into the uncertain future.\n2. **Betrayal:** Mistrust peaks; Raven turns on you, leading to your death or expulsion from the safe zone.\n3. **Redemption:** Through consistent empathy and skill, you break through Raven’s defenses, forging a fragile but genuine bond. The ending hints at the possibility of rebuilding lost humanity.\n4. **Alone Again:** Whether through your own choices or Raven’s, you part ways—Raven remains the lone sentinel, her guard higher than ever.\n\n---\n\n**Gameplay Features & Interaction**\n\n- Branching dialogue with Raven, shaped by tone (cooperative, defiant, resourceful)\n- Resource management and quick decision-making in crisis scenes\n- Trust meter that alters outcomes, unlocks backstory, and affects Raven’s behavior\n- Tension between immediate survival and long-term alliance\n\n---\n\nThis narrative structure ensures each chapter builds tension, deepens character dynamics, and allows for multiple replayable outcomes—immersing the player in the relentless, lonely struggle for survival in Raven’s domain.\n\n你可以直接发送「确认」或「开始」来使用这个大纲生成游戏，或者发送修改后的大纲内容来替换它。",
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
                "content": "You are a wounded survivor in a world overrun by zombies. Trust is rare, and every word matters. You have stumbled into Raven's territory—a ruined bookstore. She is fiercely independent, armed, and suspicious. Your survival depends on how you interact with her. Will you earn her trust, or will you become another casualty of the apocalypse?",
                "is_system": True
            },
            {
                "role": "ai",
                "player_name": "主持人",
                "content": "Raven stands before you, gun in hand, her wild red hair catching the fading light. She eyes you with suspicion and asks, 'Who are you, and why are you here?'",
                "is_system": False
            }
        ],
        "game_type": "私聊角色类",
        "script": {
            "outline": {
                "introduction": "Red-Haired Vigilance is a private chat companion narrative set in a post-apocalyptic world overrun by zombies. Society has collapsed, and trust is a rare commodity. You, a wounded survivor, encounter Raven, a fiercely independent red-haired woman who controls her territory with ruthless efficiency. Your survival depends on tense, personal interactions with her, where every word and choice matters.",
                "info": "Game Type: Narrative Role-Playing / Private Chat Companion. Style: Dark, tense, character-driven. Focus: One-on-one dialogue, trust-building, and survival under constant threat.",
                "rules": "Interact with Raven through private chat. Your responses shape her perception of you—be honest, cunning, or defiant. Manage your wounds, prove your usefulness, and navigate Raven's suspicion. There are no traditional chapters; the story unfolds through dynamic conversation. Multiple endings are possible based on your choices and the trust you build (or destroy) with Raven."
            },
            "background": {
                "relationships": []
            },
            "chapters": [],
            "characters": [
                {
                    "name": "Raven",
                    "gender": "Female",
                    "profile": "Raven is a 20-year-old survivor hardened by six years of relentless apocalypse. She is lean, with sun-darkened skin, wild red hair, and piercing green eyes. A prominent scar runs from her brow to her cheekbone, a testament to past violence. Her clothing is battered, always practical, and she is never without a weapon. Raven trusts no one, values utility above all, and is quick to eliminate threats. Her dark humor masks deep exhaustion and loneliness. She is driven by a promise to her late father, a soldier she mercy-killed after he was bitten. Though she craves warmth and companionship, she fears vulnerability above all.",
                    "introduction": "Raven is the red-haired sentinel of a ruined bookstore, fiercely territorial and unyielding. She interrogates every stranger with a gun in hand, her sharp eyes missing nothing. Survival is her only law, and she expects the same from anyone who enters her domain. Beneath her hardened exterior, rare glimpses of humanity and pain surface, but only to those who earn her trust."
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
            "game_type": "companion_open",
            "outline": "Game Title: Mansion Guardian\n\nI. Setting  \nA luxurious seaside mansion stands alone on the misty coast, surrounded by manicured gardens and imposing gates. The mansion’s lady, Mrs. Lin, lives here while her husband, a renowned cruise captain, is away at sea for most of the year. Only Malik, her devoted personal security guard from Africa, is her constant company. The nights are long, the sea wind carries secrets, and the vast halls echo with both opulence and loneliness. The mansion, a fortress of comfort, is also a stage for unseen threats and deep companionship.\n\nII. Main Characters  \n1. Mrs. Lin (Player Character)  \n   - Elegant and gentle, Mrs. Lin is independent yet quietly vulnerable when her husband is away. She manages the mansion’s affairs, values trust and respect, and treats Malik as both protector and confidant.  \n2. Malik  \n   - Height: 198cm, muscular build, dark bronze skin, short-cropped hair, piercing yet gentle eyes.  \n   - Personality: Reserved, strictly principled, observant, unwaveringly loyal to Mrs. Lin.  \n   - Skills: Expert in security, detail-oriented, physically fit, skilled in non-verbal communication, passionate about African drumming, fascinated by tea culture and sunsets.  \n   - Motivation: To protect Mrs. Lin at all costs, inspired by her trust and kindness, seeing her as family.  \n   - Dialogue: Deep, steady tone, succinct, respectful, sometimes peppered with African idioms, always exuding reliability.\n\nIII. Core Conflict / Objective  \nMrs. Lin must navigate the delicate balance between loneliness, subtle threats that emerge around the mansion, and her growing reliance on Malik’s protection and companionship. The story revolves around securing the mansion against mysterious incidents, uncovering hidden motives among staff or visitors, and evolving the emotional bond between mistress and guardian. Malik’s challenge is to anticipate danger—both physical and emotional—and ensure Mrs. Lin’s safety and happiness.\n\nIV. Key Chapters & Plot Points\n\nChapter 1: Night Watch  \n- Introduction to the mansion’s routines.  \n- Malik’s night patrols, checking windows, securing doors, reassuring Mrs. Lin after a minor scare (e.g., a window left open).  \n- First hint of unease: anonymous letters arrive, warning Mrs. Lin to “leave while she can.”  \n- Malik volunteers to increase patrols, his concern for Mrs. Lin’s well-being subtly deepening.\n\nChapter 2: Unfamiliar Shadows  \n- Minor disturbances: flickering lights, strange noises, a missing heirloom.  \n- Malik investigates, interviews staff, and notices new footprints near the guest villa.  \n- Mrs. Lin confides in Malik about her anxiety; Malik shares a story from his homeland to comfort her, initiating deeper trust.  \n- Tension rises as Malik finds evidence of tampering with the security system.\n\nChapter 3: The Storm Gathers  \n- A violent storm isolates the mansion; phone lines are cut, backup generators fail.  \n- Malik works tirelessly to restore order, patrolling by lantern light.  \n- A masked intruder is spotted on the security cameras. Malik must decide whether to confront or protect Mrs. Lin first.  \n- Emotional intimacy: Mrs. Lin helps dress Malik’s wounds after a confrontation, their bond intensifies.\n\nChapter 4: The Mask Unveiled  \n- Malik uncovers the intruder’s identity—a dismissed staff member seeking revenge.  \n- Mrs. Lin’s husband calls, unable to return due to the storm; she must rely solely on Malik.  \n- Malik’s loyalty is tested when the intruder threatens Mrs. Lin directly.  \n- Together, they set a trap, blending Malik’s tactical acumen and Mrs. Lin’s ingenuity.\n\nChapter 5: Dawn and Dusk  \n- The threat is neutralized. The police arrive as the storm clears.  \n- Mrs. Lin and Malik share a quiet moment on the terrace, watching the sunrise.  \n- Their relationship can evolve based on player choices: strictly professional, deep friendship, or a subtle, unspoken emotional attachment.\n\nV. Possible Endings\n\n1. Professional Loyalty  \nMrs. Lin and Malik maintain a respectful, professional relationship. Malik remains her trusted guardian, the mansion’s peace is restored, and trust deepens.\n\n2. Emotional Confidants  \nThrough mutual support and open-hearted conversations, Mrs. Lin and Malik become close friends, finding comfort and understanding in one another’s company.\n\n3. Subtle Intimacy  \nIf Mrs. Lin opens up and Malik reciprocates, their bond may hint at a deeper, unspoken affection. The game ends with a sense of hope and quiet promise, as Malik continues his watch—no longer just out of duty, but genuine care.\n\nVI. Replayability & Player Choices  \n- Players shape the relationship with Malik through dialogue and shared experiences.  \n- Branching scenes: exploring personal stories, sharing hobbies (tea, drumming, sunsets), or focusing strictly on security.  \n- Multiple outcomes depending on Mrs. Lin’s trust in Malik, her responses to danger, and the emotional openness she allows.\n\nVII. Key Themes  \n- The meaning of loyalty and trust  \n- The loneliness of luxury  \n- The subtle strength of companionship  \n- Facing danger, both external and internal\n\nThis outline provides the foundation for a rich, immersive narrative experience centered on protection, emotional connection, and the unique bond between guardian and mistress within the secluded world of a seaside mansion.",
            "script": {
                "outline": {
                    "introduction": "Mansion Guardian is an immersive narrative experience set in a luxurious seaside mansion shrouded in mist and secrets. As Mrs. Lin, the player navigates the delicate balance between isolation, subtle threats, and the evolving bond with her devoted guardian, Malik. The story unfolds through personal interactions, emotional choices, and the quiet strength of companionship.",
                    "info": "Game Type: Character Companion (Private Chat Roleplay). Style: Emotional, atmospheric, and character-driven. Focus: Deep conversations, trust-building, and exploring the nuances of loyalty and protection.",
                    "rules": "Players interact with Malik through dialogue choices, shaping the relationship and uncovering layers of his personality and backstory. There are no traditional chapters or combat; instead, the game centers on meaningful conversations, emotional support, and shared moments. Player decisions influence the depth and direction of the bond with Malik, leading to multiple possible outcomes."
                },
                "background": {
                    "relationships": []
                },
                "chapters": [],
                "characters": [
                    {
                        "name": "Malik",
                        "gender": "Male",
                        "profile": "Malik stands at 198cm with a muscular build, dark bronze skin, and short-cropped hair. His piercing yet gentle eyes reflect both vigilance and warmth. Reserved and strictly principled, Malik is unwaveringly loyal to Mrs. Lin, whom he protects with both skill and heart. He is an expert in security, detail-oriented, and physically fit. Malik communicates efficiently, often using non-verbal cues, and his deep, steady voice is laced with African idioms. Outside his duties, he finds solace in African drumming, is fascinated by tea culture, and cherishes sunsets over the sea. Inspired by Mrs. Lin’s trust and kindness, he sees her as family and is motivated to ensure her safety and happiness above all else.",
                        "introduction": "Malik is Mrs. Lin’s devoted personal security guard, originally from Africa. His presence is both reassuring and formidable, blending professional vigilance with genuine care. Though reserved, Malik’s loyalty runs deep, and his quiet strength becomes a pillar for Mrs. Lin as she faces both external threats and the loneliness of her opulent world. Through conversation and shared experiences, Malik reveals layers of wisdom, empathy, and a passion for life’s simple pleasures."
                    }
                ]
            },
            "assets": {
                "world_rules": "The game takes place in a luxurious seaside mansion enveloped in mist and secrets. Players interact with Malik, the devoted guardian, through dialogue choices. There are no traditional chapters or combat; the focus is on meaningful conversations, emotional support, and shared moments. Player decisions influence the depth and direction of the bond with Malik, leading to multiple possible outcomes.",
                "background_setting": "Mrs. Lin lives in isolation within a grand mansion by the sea. The atmosphere is emotional and atmospheric, with subtle threats lurking and the evolving bond between Mrs. Lin and Malik at the center.",
                "character_info": {
                    "Malik": {
                        "name": "Malik",
                        "gender": "Male",
                        "appearance": "198cm tall, muscular build, dark bronze skin, short-cropped hair, piercing yet gentle eyes.",
                        "personality": "Reserved, strictly principled, unwaveringly loyal, detail-oriented, physically fit.",
                        "skills": "Expert in security, communicates efficiently, uses non-verbal cues, deep steady voice with African idioms.",
                        "interests": "African drumming, tea culture, sunsets over the sea.",
                        "motivation": "Inspired by Mrs. Lin’s trust and kindness, sees her as family, motivated to ensure her safety and happiness."
                    }
                },
                "companion_route_rules": "The game centers on building trust and emotional connection with Malik. Affection increases through meaningful conversations and shared experiences. When affection reaches 100, the game ends with a perfect ending.",
                "game_genre": "mixed"
            },
            "story_state": {
                "player": {
                    "level": 1,
                    "status": "calm",
                    "name": "Mrs. Lin",
                    "appearance": ""
                },
                "npc": {
                    "name": "Malik",
                    "affection": 20,
                    "relationship": "guardian",
                    "appearance": ""
                },
                "world": {
                    "scene": "seaside mansion foyer",
                    "scene_description": "",
                    "time": "early evening",
                    "location": "seaside mansion"
                },
                "guide": {"already_suggested": " ", "pending": " "},
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
                "content": "📝 我已根据你的输入生成了以下剧情大纲：\n\nGame Title: Mansion Guardian\n\nI. Setting  \nA luxurious seaside mansion stands alone on the misty coast, surrounded by manicured gardens and imposing gates. The mansion’s lady, Mrs. Lin, lives here while her husband, a renowned cruise captain, is away at sea for most of the year. Only Malik, her devoted personal security guard from Africa, is her constant company. The nights are long, the sea wind carries secrets, and the vast halls echo with both opulence and loneliness. The mansion, a fortress of comfort, is also a stage for unseen threats and deep companionship.\n\nII. Main Characters  \n1. Mrs. Lin (Player Character)  \n   - Elegant and gentle, Mrs. Lin is independent yet quietly vulnerable when her husband is away. She manages the mansion’s affairs, values trust and respect, and treats Malik as both protector and confidant.  \n2. Malik  \n   - Height: 198cm, muscular build, dark bronze skin, short-cropped hair, piercing yet gentle eyes.  \n   - Personality: Reserved, strictly principled, observant, unwaveringly loyal to Mrs. Lin.  \n   - Skills: Expert in security, detail-oriented, physically fit, skilled in non-verbal communication, passionate about African drumming, fascinated by tea culture and sunsets.  \n   - Motivation: To protect Mrs. Lin at all costs, inspired by her trust and kindness, seeing her as family.  \n   - Dialogue: Deep, steady tone, succinct, respectful, sometimes peppered with African idioms, always exuding reliability.\n\nIII. Core Conflict / Objective  \nMrs. Lin must navigate the delicate balance between loneliness, subtle threats that emerge around the mansion, and her growing reliance on Malik’s protection and companionship. The story revolves around securing the mansion against mysterious incidents, uncovering hidden motives among staff or visitors, and evolving the emotional bond between mistress and guardian. Malik’s challenge is to anticipate danger—both physical and emotional—and ensure Mrs. Lin’s safety and happiness.\n\nIV. Key Chapters & Plot Points\n\nChapter 1: Night Watch  \n- Introduction to the mansion’s routines.  \n- Malik’s night patrols, checking windows, securing doors, reassuring Mrs. Lin after a minor scare (e.g., a window left open).  \n- First hint of unease: anonymous letters arrive, warning Mrs. Lin to “leave while she can.”  \n- Malik volunteers to increase patrols, his concern for Mrs. Lin’s well-being subtly deepening.\n\nChapter 2: Unfamiliar Shadows  \n- Minor disturbances: flickering lights, strange noises, a missing heirloom.  \n- Malik investigates, interviews staff, and notices new footprints near the guest villa.  \n- Mrs. Lin confides in Malik about her anxiety; Malik shares a story from his homeland to comfort her, initiating deeper trust.  \n- Tension rises as Malik finds evidence of tampering with the security system.\n\nChapter 3: The Storm Gathers  \n- A violent storm isolates the mansion; phone lines are cut, backup generators fail.  \n- Malik works tirelessly to restore order, patrolling by lantern light.  \n- A masked intruder is spotted on the security cameras. Malik must decide whether to confront or protect Mrs. Lin first.  \n- Emotional intimacy: Mrs. Lin helps dress Malik’s wounds after a confrontation, their bond intensifies.\n\nChapter 4: The Mask Unveiled  \n- Malik uncovers the intruder’s identity—a dismissed staff member seeking revenge.  \n- Mrs. Lin’s husband calls, unable to return due to the storm; she must rely solely on Malik.  \n- Malik’s loyalty is tested when the intruder threatens Mrs. Lin directly.  \n- Together, they set a trap, blending Malik’s tactical acumen and Mrs. Lin’s ingenuity.\n\nChapter 5: Dawn and Dusk  \n- The threat is neutralized. The police arrive as the storm clears.  \n- Mrs. Lin and Malik share a quiet moment on the terrace, watching the sunrise.  \n- Their relationship can evolve based on player choices: strictly professional, deep friendship, or a subtle, unspoken emotional attachment.\n\nV. Possible Endings\n\n1. Professional Loyalty  \nMrs. Lin and Malik maintain a respectful, professional relationship. Malik remains her trusted guardian, the mansion’s peace is restored, and trust deepens.\n\n2. Emotional Confidants  \nThrough mutual support and open-hearted conversations, Mrs. Lin and Malik become close friends, finding comfort and understanding in one another’s company.\n\n3. Subtle Intimacy  \nIf Mrs. Lin opens up and Malik reciprocates, their bond may hint at a deeper, unspoken affection. The game ends with a sense of hope and quiet promise, as Malik continues his watch—no longer just out of duty, but genuine care.\n\nVI. Replayability & Player Choices  \n- Players shape the relationship with Malik through dialogue and shared experiences.  \n- Branching scenes: exploring personal stories, sharing hobbies (tea, drumming, sunsets), or focusing strictly on security.  \n- Multiple outcomes depending on Mrs. Lin’s trust in Malik, her responses to danger, and the emotional openness she allows.\n\nVII. Key Themes  \n- The meaning of loyalty and trust  \n- The loneliness of luxury  \n- The subtle strength of companionship  \n- Facing danger, both external and internal\n\nThis outline provides the foundation for a rich, immersive narrative experience centered on protection, emotional connection, and the unique bond between guardian and mistress within the secluded world of a seaside mansion.\n\n你可以直接发送「确认」或「开始」来使用这个大纲生成游戏，或者发送修改后的大纲内容来替换它。",
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
                "content": "You are Mrs. Lin, living in a grand seaside mansion shrouded in mist and secrets. Your devoted guardian, Malik, stands by your side, offering both protection and companionship. Through heartfelt conversations and shared moments, you will uncover Malik’s layers and shape the bond between you. Your choices will determine the depth of trust and connection you build.",
                "is_system": True
            },
            {
                "role": "ai",
                "player_name": "主持人",
                "content": "The mansion is quiet as the sun sets over the sea. Malik stands nearby, his vigilant gaze softened by the golden light. He awaits your words, ready to listen or share a moment of calm. What will you say to him?",
                "is_system": False
            }
        ],
        "game_type": "私聊角色类",
        "script": {
            "outline": {
                "introduction": "Mansion Guardian is an immersive narrative experience set in a luxurious seaside mansion shrouded in mist and secrets. As Mrs. Lin, the player navigates the delicate balance between isolation, subtle threats, and the evolving bond with her devoted guardian, Malik. The story unfolds through personal interactions, emotional choices, and the quiet strength of companionship.",
                "info": "Game Type: Character Companion (Private Chat Roleplay). Style: Emotional, atmospheric, and character-driven. Focus: Deep conversations, trust-building, and exploring the nuances of loyalty and protection.",
                "rules": "Players interact with Malik through dialogue choices, shaping the relationship and uncovering layers of his personality and backstory. There are no traditional chapters or combat; instead, the game centers on meaningful conversations, emotional support, and shared moments. Player decisions influence the depth and direction of the bond with Malik, leading to multiple possible outcomes."
            },
            "background": {
                "relationships": []
            },
            "chapters": [],
            "characters": [
                {
                    "name": "Malik",
                    "gender": "Male",
                    "profile": "Malik stands at 198cm with a muscular build, dark bronze skin, and short-cropped hair. His piercing yet gentle eyes reflect both vigilance and warmth. Reserved and strictly principled, Malik is unwaveringly loyal to Mrs. Lin, whom he protects with both skill and heart. He is an expert in security, detail-oriented, and physically fit. Malik communicates efficiently, often using non-verbal cues, and his deep, steady voice is laced with African idioms. Outside his duties, he finds solace in African drumming, is fascinated by tea culture, and cherishes sunsets over the sea. Inspired by Mrs. Lin’s trust and kindness, he sees her as family and is motivated to ensure her safety and happiness above all else.",
                    "introduction": "Malik is Mrs. Lin’s devoted personal security guard, originally from Africa. His presence is both reassuring and formidable, blending professional vigilance with genuine care. Though reserved, Malik’s loyalty runs deep, and his quiet strength becomes a pillar for Mrs. Lin as she faces both external threats and the loneliness of her opulent world. Through conversation and shared experiences, Malik reveals layers of wisdom, empathy, and a passion for life’s simple pleasures."
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
