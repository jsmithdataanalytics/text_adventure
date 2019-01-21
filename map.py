#!/usr/bin/env python

"""map.py: Defines the game data."""

__author__ = "James Smith"

game_map = {
  "command_history": ["get all", "open", "get all", "down", "out", "east", "north", "get all", "south", "get all", "dig", "get all", "in", "out", "north", "west", "in", "get all", "out", "cut", "north", "", "", "west", "attack goblin with sword", "", "east", "north", "get all", "south", "", "", "", "", "in", "out", "north", "", "", "", "", "south", "west", "", "south", "", "attack goblin with dot", "west", "", "attack troll with dot", "get all", "west", "get all", "east", "", "", "north", "", "east", "", "south", "", "", "in", "show the flowers to the potion master", "look", "out", "in", "east", "west", "out", "east", "south", "", "north", "east", "north", "east", "go inside"],
  "opening": {
    "title": "THE VISTA",
    "intro": [
      "Welcome to The Vista, a retro text adventure.",
      "In this game, you'll explore the fantasy realm known only as \"The Vista\". You'll do so via a simple text interface, typing commands and receiving text responses. As with every text-based game, you have to provide commands that the game can recognise, which can involve some guesswork. The best strategy is to keep it simple. Pretty much every command in the game is four words or fewer, e.g. \"go north\", \"get sword\", \"drop all\", \"look around\", \"check inventory\", \"attack goblin with sword\" etc. So basically just \"verb noun\", or occasionally \"verb noun with noun\". You get the idea.\n\nType \"commands\" to see a list of example commands. Hit enter to repeat the previous command. Type \"quit\" to exit the game. Now, let's set the scene...",
      "Fade in.",
      "We start with a traditional, twee fantasy village... Floonyloon Village. It's like The Shire, but without the hairy feet. Enter our hero:... wait, what's your name?",
      "Nice. Enter our hero, {name}. You're a young lad or lass, living in the village. Like 9 or 10 years old. The kind of age where your parents definitely shouldn't be letting you go off on dangerous adventures without supervision, but for some reason that doesn't seem to matter here.",
      "You're a stoic, quiet kid. A real Thomas Anderson. Very easy from a dialogue writing perspective.",
      "You've just woken up at home..."
    ]
  },
  "layout": [
    [
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "home1", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"]
    ],
    [
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "apoth", "block", "block", "mohut", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "homeg", "block", "jimbg", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"]
    ],
    [
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "treeh", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"]
    ],
    [
      ["block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "block", "block", "deade", "block", "block", "cave1", "block", "block", "block"],
      ["block", "block", "block", "wood5", "wood4", "wood3", "block", "block", "block", "block", "block", "block"],
      ["block", "block", "block", "wood6", "block", "wood2", "block", "moua3", "moub3", "mouc3", "block", "block"],
      ["dingl", "wood9", "wood8", "wood7", "block", "wood1", "block", "moua2", "moub2", "mouc2", "block", "block"],
      ["block", "block", "dead2", "block", "block", "vila2", "vilb2", "moua1", "moub1", "mouc1", "block", "block"],
      ["block", "block", "block", "block", "block", "vila1", "vilb1", "block", "block", "block", "block", "block"],
      ["magma", "magma", "magma", "magma", "magma", "block", "spath", "block", "ocean", "ocean", "ocean", "ocean"],
      ["magma", "magma", "magma", "magma", "magma", "block", "shrin", "block", "ocean", "ocean", "ocean", "ocean"],
      ["magma", "magma", "magma", "magma", "magma", "block", "block", "block", "ocean", "ocean", "ocean", "ocean"],
      ["magma", "magma", "magma", "magma", "magma", "block", "block", "ocean", "ocean", "ocean", "ocean", "ocean"],
      ["magma", "magma", "magma", "magma", "magma", "block", "block", "ocean", "ocean", "ocean", "ocean", "ocean"]
    ]
  ],
  "spawn_point": [0, 6, 5],
  "rooms": {
    "block": {
      "name": "block",
      "text": {
        "init_core": "You shouldn't be here."
      },
      "items": [],
      "state": {}
    },
    "woods": {
      "name": "woods",
      "text": {
        "init_core": "You are in a forest."
      },
      "items": [],
      "state": {}
    },
    "ocean": {
      "name": "ocean",
      "text": {
        "init_core": "You are on the ocean floor."
      },
      "items": [],
      "state": {}
    },
    "mount": {
      "name": "mount",
      "text": {
        "init_core": "You are in the mountains."
      },
      "items": [],
      "state": {}
    },
    "moua1": {
      "name": "moua1",
      "text": {
        "init_core": "You have reached the Gygax Mountains. The vast mountain range sprawls out before you, covered in a thick blanket of snow. You can travel north or east to go further into the mountains, or go west to return to Floonyloon Village.",
        "short_core": "You are in the Gygax Mountains. You can travel north or east to go further into the mountains, or go west to return to Floonyloon Village.",
        "long_core": "You are in the Gygax Mountains. The vast mountain range sprawls out to the north and east, covered in a thick blanket of snow. Floonyloon Village lies to the west.",
        "state": {},
        "responses": {}
      },
      "items": [],
      "state": {},
      "blocks": []
    },
    "moua2": {
      "name": "moua2",
      "text": {
        "init_core": "You are in the mountains. You can travel north, south, or east from here.",
        "state": {},
        "responses": {}
      },
      "items": [],
      "enemies": ["moua2wolf"],
      "state": {},
      "blocks": []
    },
    "moua3": {
      "name": "moua3",
      "text": {
        "init_core": "You are in the mountains. You can travel south or east from here.",
        "state": {},
        "responses": {}
      },
      "items": [],
      "state": {},
      "blocks": []
    },
    "moub1": {
      "name": "moub1",
      "text": {
        "init_core": "You are in the mountains. You can travel north or west from here. To the east, there is a steep, icy incline, which might be climbable were you to wear some kind of snow boots.",
        "state": {},
        "responses": {}
      },
      "items": ["sticks"],
      "state": {},
      "blocks": []
    },
    "moub2": {
      "name": "moub2",
      "text": {
        "init_core": "You are in the mountains, stood just outside a small mountain hut.",
        "state": {
          "frozen": {
            "0": "The door is wide open, and there seems to be a fire burning inside.",
            "1": "It seems to be frozen solid, but the door is wide open."
          }
        },
        "responses": {}
      },
      "items": [],
      "state": {
        "frozen": 1,
        "extra_directions": {
          "in": [1, 4, 8],
          "aliases": ["(the +)?(small +)?(mountain +)?hut"]
        }
      },
      "blocks": ["north", "east"]
    },
    "moub3": {
      "name": "moub3",
      "text": {
        "init_core": "You are surrounded by tall, unclimbable rock faces in all directions, except to the west.",
        "state": {
          "cave": {
            "0": "",
            "1": "However, the avalanches seem to have revealed an entrance to a hidden cave in one of the walls."
          }
        },
        "responses": {}
      },
      "items": ["matchbook"],
      "enemies": ["moub3wolf"],
      "state": {
        "cave": 0
      },
      "blocks": ["south", "east"]
    },
    "cave1": {
      "name": "cave1",
      "text": {
        "init_core": "You are inside the secret cave. It's a large, round room with a high ceiling. The light from outside dances over the walls and ceiling as it reflects off a circular pool of crystal clear water, which occupies most of the floorspace. This must be the fabled Alaria Spring Water!"
      },
      "items": [],
      "enemies": [],
      "state": {
        "extra_directions": {
          "out": [3, 3, 8],
          "aliases": ["(the +)?((secret|hidden) +)?cave(rn)?"]
        }
      },
      "blocks": []
    },
    "mouc1": {
      "name": "mouc1",
      "text": {
        "init_core": "You are high up in the mountains. To the north, there is a steep, icy incline. An equally treacherous, downward slope leads west.",
        "state": {},
        "responses": {}
      },
      "items": [],
      "state": {},
      "blocks": []
    },
    "mouc2": {
      "name": "mouc2",
      "text": {
        "init_core": "You are at the peak of the Gygax Mountains. The view from here would be spectacular, were you not stood in the middle of a blizzard, complete with frequent claps of thunder. The summit is a flat platform, suitable for use as a fighting arena.",
        "short_core": "You are at the flat peak of the Gygax Mountains. From here you can travel north, or head south to begin your descent.",
        "long_core": "You are at the flat peak of the Gygax Mountains. The view from here would be spectacular, were you not stood in the middle of a blizzard. From here you can travel north, or head south to begin your descent.",
        "state": {},
        "responses": {}
      },
      "items": ["citrine", "hammer"],
      "enemies": ["mouc2giant"],
      "state": {},
      "blocks": ["west"]
    },
    "mouc3": {
      "name": "mouc3",
      "text": {
        "init_core": "You are atop the Gygax Mountains. You are at a dead end, with sheer drops on all sides, except to the south. Set into the ground is a circular stone pedestal, which bears an engraving in the shape of a hammer.",
        "state": {},
        "responses": {}
      },
      "items": [],
      "state": {},
      "blocks": ["west"]
    },
    "mohut": {
      "name": "mohut",
      "text": {
        "init_core": "You are inside the mountain hut.",
        "state": {
          "frozen": {
            "0": "There is a hearty fire burning in the fireplace, and a chest in the corner...",
            "1": "All the furniture is frozen, including the chest in the corner."
          },
          "firewood": {
            "0": "There is an empty fireplace, which looks like it hasn't been used in years.",
            "1": "There is an old fireplace with some firewood in it.",
            "2": ""
          },
          "open": {
            "0": "",
            "1": "it's open.",
            "2": "it's empty."
          }
        }
      },
      "items": ["snow boots"],
      "state_order": ["frozen", "firewood", "open", "extra_directions"],
      "state": {
        "frozen": 1,
        "firewood": 0,
        "open": 0,
        "extra_directions": {
          "out": [3, 4, 8],
          "aliases": ["(the +)?(small +)?(mountain +)?hut"]
        }
      }
    },
    "magma": {
      "name": "magma",
      "text": {
        "init_core": "You are on an active volcano."
      },
      "items": [],
      "state": {}
    },
    "vila1": {
      "name": "vila1",
      "text": {
        "init_core": "You're in the southwest part of Floonyloon Village, right outside your house. Normally you'd be met by sunshine, birdsong, and a dozen cheery greetings from impossibly upbeat neighbours. But something is different today. Dark clouds cover the land in all directions, and there doesn't seem to be a soul in sight. You'd better go find your buddy, Jimbo, and see if he knows what's going on. He lives in the southeast part of town. Paths lead east and north from here.",
        "short_core": "You're in the southwest part of Floonyloon Village, right next to your house. Paths lead east and north from here.",
        "long_core": "You're in the southwest part of Floonyloon Village, right outside your house. Usually the village is a happy and upbeat place, but something seems different today. Dark clouds cover the land in all directions, and there doesn't seem to be a soul in sight. Paths lead east and north from here."
      },
      "items": [],
      "state": {
        "extra_directions": {
          "in": [1, 6, 5],
          "aliases": ["((the|your|my) +)?house", "{player_name}'?s?( +house)?"]
        }
      }
    },
    "home1": {
      "name": "home1",
      "text": {
        "init_core": "You're in the bedroom of your house. There's a rickety wooden staircase leading down,",
        "state": {
          "opened": {
            "0": "and a chest in the corner.",
            "1": "and an open chest in the corner."
          }
        },
        "responses": {
          "locked": "It's locked. You need the key!",
          "unlocked": "The chest springs open to reveal",
          "already_opened": "It's already open you mug.",
          "already_unlocked": "It's already open you mug.",
          "no_key": "You need a key to do that."
        }
      },
      "items": ["ruby", "key"],
      "state": {
        "opened": 0,
        "locked": 1,
        "extra_directions": {
          "downstairs": None
        }
      }
    },
    "homeg": {
      "name": "homeg",
      "text": {
        "init_core": "You are in the living room of your house. A wooden staircase leads up from here, and a door leads outside."
      },
      "items": [],
      "state": {
        "extra_directions": {
          "upstairs": None,
          "out": [3, 6, 5],
          "aliases": ["((the|your|my) +)?house", "{player_name}'?s?( +house)?"]
        }
      }
    },
    "vila2": {
      "name": "vila2",
      "text": {
        "init_core": "This is the northwest part of the village, where the Potion Master's apothecary is. It's a weird tipi thing, made of all sorts of exotic plants and animal skins. Plumes of brightly coloured smoke rise from the top.\n\nTo the north, a path leads into Robinett Forest. There are also paths leading east and south from here.",
        "short_core": "This is the northwest part of the village, where the Potion Master's apothecary is. To the north, a path leads into Robinett Forest. There are also paths leading east and south from here.",
        "long_core": "This is the northwest part of Floonyloon Village, where the Potion Master's apothecary is. It's a weird tipi thing, made of all sorts of exotic plants and animal skins. Plumes of brightly coloured smoke rise from the top.\n\nTo the north, a path leads into Robinett Forest. There are also paths leading east and south from here.",
        "state": {
          "cut": {
            "0": "The northward path is obstructed by a thicket of thorny vines.",
            "1": ""
          }
        },
        "responses": {
          "already_cut": "You've already cut the vines away you mug.",
          "cut_success": "You've successfully cut away the vines, revealing a path into the forest.",
          "nothing_to_cut_with": "You have nothing to cut with."
        }
      },
      "items": [],
      "state": {
        "extra_directions": {
          "in": [1, 4, 5],
          "aliases": ["(the +)?potion +master('?s)?( +(house|tipi|teepee|tent|apothecary))?", "(the +)?(house|tipi|teepee|tent|apothecary)"]
        },
        "cut": 0
      },
      "blocks": ["north"]
    },
    "apoth": {
      "name": "apoth",
      "text": {
        "init_core": "You're inside the Potion Master's tent. The Potion Master is stood over a large cauldron, mixing some kind of red coloured elixir.\n\n\"Huh? What are you doing here {name}? You should be resting! What do you mean you're not sick? Everyone is, even me! Amazing, you must have some kind of natural resilience...\"\n\n\"This land is cursed, {name}. Strange creatures are invading The Vista, using evil magic to transform it into a world of darkness and despair. The only way to stop the onslaught is to gather the three precious orbs hidden throughout the land...\"\n\n\"The Blue Orb, hidden deep in Robinett Forest...\"\n\"The Yellow Orb, lost in the Gygax Mountains...\"\n\"The Red Orb, whose resting place is unknown...\"\n\n\"{name}, you must find the orbs and vanquish the rising evil!\"\n\n\"In the the meantime, I can make a potion to cure everyone here, but I need some pretty rare ingredients. The kind of stuff you just can't find here in town. I need you to bring back some Dingleflowers from the forest, and some Alaria Spring Water from the mountains.\"\n\n\"Head to the forest first, find the Blue Orb, and bring me some Dingleflowers! I'm counting on you, {name}!\"\n\nThe Potion Master then returns to work, hastily throwing more ingredients into the cauldron.",
        "short_core": "You're in the Potion Master's tent. She says: \"{name}, go to Robinett Forest, find the Blue Orb, and bring me some Dingleflowers!",
        "long_core": "You're inside the Potion Master's tent. The Potion Master is stood over a large cauldron, mixing some kind of red coloured elixir.\n\n\"Huh? What are you doing here {name}? You should be resting! What do you mean you're not sick? Everyone is, even me! Amazing, you must have some kind of natural resilience...\"\n\n\"This land is cursed, {name}. Strange creatures are invading The Vista, using evil magic to transform it into a world of darkness and despair. The only way to stop the onslaught is to gather the three precious orbs hidden throughout the land...\"\n\n\"The Blue Orb, hidden deep in Robinett Forest...\"\n\"The Yellow Orb, lost in the Gygax Mountains...\"\n\"The Red Orb, whose resting place is unknown...\"\n\n\"{name}, you must find the orbs and vanquish the rising evil!\"\n\n\"In the the meantime, I can make a potion to cure everyone here, but I need some pretty rare ingredients. The kind of stuff you just can't find here in town. I need you to bring back some Dingleflowers from the forest, and some Alaria Spring Water from the mountains.\"\n\n\"Head to the forest first, find the Blue Orb, and bring me some Dingleflowers! I'm counting on you, {name}!\"\n\nThe Potion Master then returns to work, hastily throwing more ingredients into the cauldron.",
        "short_core2": "You're in the Potion Master's tent. She says: \"{name}, you must now go to the Gygax Mountains, find the Yellow Orb, and bring me some Alaria Spring Water! Hurry!\"\n\nThe Potion Master then returns to work, hastily throwing more ingredients into the cauldron.",
        "long_core2": "You're inside the Potion Master's tent. The Potion Master is stood over a large cauldron, mixing some kind of red coloured elixir. She says: \"{name}, you must now go to the Gygax Mountains, find the Yellow Orb, and bring me some Alaria Spring Water! Hurry!\"\n\nThe Potion Master then returns to work, hastily throwing more ingredients into the cauldron.",
        "short_core3": "You're in the Potion Master's tent. She says: \"{name}, take the orbs to the temple near Jimbo's house and break this curse once and for all! You did find all three orbs, didn't you?\"",
        "long_core3": "You're in the Potion Master's tent. She says: \"{name}, take the orbs to the temple near Jimbo's house and break this curse once and for all! You did find all three orbs, didn't you?\"",
        "state": {},
        "responses": {
          "dingleflowers": "Potion Master: \"Ah! Dingleflowers! Excellent work, {name}! I'll add them to the potion right away!\"\n\nThe Potion Master takes the flowers, and tosses them into the cauldron. The potion immediately turns from red to blue.\n\n\"Yes, yes, that's right. Great work, {name}! Now, head to the Gygax Mountains, find the Yellow Orb, and bring me some Alaria Spring Water!\"",
          "water": "Potion Master: \"Ah! Alaria Spring Water! Excellent work, {name}! I'll add it to the potion right away!\"\n\nThe Potion Master takes the bottle, and empties it into the cauldron. The potion effervesces, and the colour turns from blue to shimmering gold.\n\n\"Eureka! It worked! The potion is ready, {name}! I'll take it to everyone in town, and you go to the temple near Jimbo's house and break this curse once and for all! You did find all three orbs, didn't you?\""
        }
      },
      "items": ["book", "bottle"],
      "state": {
        "extra_directions": {
          "out": [3, 5, 5],
          "aliases": ["(the +)?potion +master('?s)?( +(house|tipi|teepee|tent|apothecary))?", "(the +)?(house|tipi|teepee|tent|apothecary)"]
        }
      }
    },
    "vilb1": {
      "name": "vilb1",
      "text": {
        "init_core": "You are in the southeast part of the village, right outside Jimbo's house. The earth is soft here. Paths lead to the north, south, and west.",
        "state": {
          "dug": {
            "0": "",
            "1": "At your feet there is a small hole."
          }
        },
        "responses": {
          "already_dug": "You can't dig any further."
        }
      },
      "items": ["sword"],
      "blocks": ["south"],
      "state": {
        "extra_directions": {
          "in": [1, 6, 7],
          "aliases": ["jimbo('?s)?( +house)?", "(the +)?house"]
        },
        "dug": 0
      }
    },
    "jimbg": {
      "name": "jimbg",
      "text": {
        "init_core": "You're inside Jimbo's place. He's in bed, looking all gaunt and sick. He starts to talk in a hoarse voice, and he's all like:\n\n\"Ugh, {name}, is that you? How's it going buddy? How come you're not sick? You're like the only one in town dude! Everyone else woke up today feeling like shit, plus the weather's all messed up. There were even rumours of monsters in the forest!\"\n\n\"I dunno what's going on man, but since you're looking so sprightly, could you go and see the Potion Master on the other side of town? She at least might be able to mix something up to make everyone feel better.\"\n\n\"Oh, and take my sword with you, just in case. I buried it just outside the house, so the monsters don't find it. You'll need a shovel... I think I saw one lying around somewhere in town, but you might need to explore a little.\"\n\nJimbo's counting on you. You'd better work with the Potion Master to rustle something up.",
        "short_core": "This is Jimbo's house. He says: \"Go see the Potion Master and help her cook something up for everyone!\"",
        "state": {}
      },
      "items": [],
      "state": {
        "extra_directions": {
          "out": [3, 6, 6],
          "aliases": ["jimbo('?s)?( +house)?", "(the +)?house"]
        }
      }
    },
    "vilb2": {
      "name": "vilb2",
      "text": {
        "init_core": "You are in the northeast part of the village. All the shops are closed, so you won't be able to get any supplies here. Paths run south, west, and east."
      },
      "items": ["shovel"],
      "blocks": ["east"],
      "state": {}
    },
    "wood1": {
      "name": "wood1",
      "text": {
        "init_core": "You have entered Robinett Forest. You are surrounded by strange, twisted trees, which tower above you and block out almost all sunlight. Dense thickets block your ways east and west, leaving only a northward path.",
        "short_core": "You are just inside the forest. Floonyloon Village lies to the south, and a path into the forest runs north.",
        "long_core": "You are just inside Robinett Forest. You are surrounded by strange, twisted trees, which tower above you and block out almost all sunlight. Dense thickets block your ways east and west, leaving only a northward path into the forest, and a southward exit into Floonyloon Village."
      },
      "items": [],
      "state": {}
    },
    "wood2": {
      "name": "wood2",
      "text": {
        "init_core": "You have moved further into the forest. Paths run north and south from here.",
        "short_core": "You are in the forest. Paths run north and south from here.",
        "long_core": "You are in Robinett Forest. You are surrounded by strange, twisted trees, which tower above you and block out almost all sunlight. Dense thickets block your ways east and west, leaving only a north-south path."
      },
      "items": [],
      "state": {}
    },
    "wood3": {
      "name": "wood3",
      "text": {
        "init_core": "You have moved further into the forest. Paths run north, south, and west from here.",
        "short_core": "You are in the forest. Paths run north, south, and west from here.",
        "long_core": "You are in Robinett Forest. You are surrounded by strange, twisted trees, which tower above you and block out almost all sunlight. Paths run north, south, and west from here."
      },
      "items": [],
      "state": {}
    },
    "wood4": {
      "name": "wood4",
      "text": {
        "init_core": "You have moved into a clearing, with paths leaving to the east and west.",
        "long_core": "You are in Robinett Forest. You are surrounded by strange, twisted trees, which tower above you and block out almost all sunlight. You are in a clearing, with paths leaving to the east and west."
      },
      "items": [],
      "enemies": ["wood4goblin"],
      "state": {}
    },
    "wood5": {
      "name": "wood5",
      "text": {
        "init_core": "You have moved further into the forest. Paths run south and east from here.",
        "short_core": "You are in the forest. Paths run south and east from here.",
        "long_core": "You are in Robinett Forest. You are surrounded by strange, twisted trees, which tower above you and block out almost all sunlight. Paths run south and east from here."
      },
      "items": [],
      "state": {}
    },
    "wood6": {
      "name": "wood6",
      "text": {
        "init_core": "You have moved further into the forest. Paths run north and south from here. A sign reads: \"Are you remembering the way? All who lose their way in these woods will perish!\"",
        "short_core": "You are in the forest. Paths run north and south from here. A sign reads: \"Are you remembering the way? All who lose their way in these woods will perish!\"",
        "long_core": "You are in Robinett Forest. You are surrounded by strange, twisted trees, which tower above you and block out almost all sunlight. Paths run north and south from here. A sign reads: \"Are you remembering the way? All who lose their way in these woods will perish!\""
      },
      "items": [],
      "state": {}
    },
    "wood7": {
      "name": "wood7",
      "text": {
        "init_core": "You have moved further into the forest. Paths run north and west from here.",
        "short_core": "You are in the forest. Paths run north and west from here.",
        "long_core": "You are in Robinett Forest. You are surrounded by strange, twisted trees, which tower above you and block out almost all sunlight. Paths run north and west from here."
      },
      "items": [],
      "enemies": ["wood7goblin"],
      "state": {}
    },
    "wood8": {
      "name": "wood8",
      "text": {
        "init_core": "You have moved further into the forest. Paths run east, west, and south from here.",
        "short_core": "You are in the forest. Paths run east, west, and south from here.",
        "long_core": "You are in Robinett Forest. You are surrounded by strange, twisted trees, which tower above you and block out almost all sunlight. Paths run east, west, and south from here."
      },
      "items": [],
      "state": {}
    },
    "wood9": {
      "name": "wood9",
      "text": {
        "init_core": "You have moved further into the forest. Paths run east and west from here.",
        "short_core": "You are in the forest. Paths run east and west from here.",
        "long_core": "You are in Robinett Forest. You are surrounded by strange, twisted trees, which tower above you and block out almost all sunlight. Paths run east and west from here."
      },
      "items": ["sapphire", "axe"],
      "enemies": ["wood9troll"],
      "state": {}
    },
    "deade": {
      "name": "deade",
      "text": {
        "init_core": "This is a dead-end."
      },
      "items": ["dot"],
      "state": {}
    },
    "dead2": {
      "name": "dead2",
      "text": {
        "init_core": "This is a dead-end. One of the trees here has some low branches. You can leave via a path to the north."
      },
      "items": [],
      "state": {}
    },
    "treeh": {
      "name": "treeh",
      "text": {
        "init_core": "You are in an abandoned treehouse, apparently built by the young kid stood in front of you. He says: \"I heard the monsters talking about taking over The Vista! Oh, and there was some stuff about three precious stones, which apparently can be used to stop them or something?\""
      },
      "items": [],
      "state": {}
    },
    "dingl": {
      "name": "dingl",
      "text": {
        "init_core": "You have reached the end of the forest trail. The path opens out into a clearing, filled with all sorts of exotic plants and flowers."
      },
      "items": ["dingleflowers"],
      "state": {}
    },
    "spath": {
      "name": "tpath",
      "text": {
        "init_core": "You are on a woodland path, to the south of Floonyloon Village. The path is lined on either side with statues honouring The Vista's greatest historical leaders. You can go north or south from here."
      },
      "items": [],
      "state": {}
    },
    "shrin": {
      "name": "shrin",
      "text": {
        "init_core": "You are in The Shrine Of The Elders, a woodland shrine to the earliest settlers of The Vista. The shrine is filled with stone tablets inscribed with Vista folklore, and statues depicting the wise leaders of those times. In the middle of it all is a stone altar, upon which are three stone pedestals, each shaped to accommodate a small, spherical object."
      },
      "items": [],
      "state": {
        "orbs": 0
      }
    }
  },
  "items": {
    "shovel": {
      "name": "Shovel",
      "aliases": ["the +shovel", "spade", "the +spade"],
      "text": {
        "init_desc": "You notice a shovel lying on the ground nearby."
      },
      "visible": 1
    },
    "key": {
      "name": "Key",
      "aliases": ["the +key"],
      "text": {
        "init_desc": "There is also a key on a nearby table."
      },
      "visible": 1
    },
    "sword": {
      "name": "Sword",
      "aliases": ["the +sword"],
      "text": {
        "init_desc": "Inside is a majestic sword."
      },
      "visible": 0
    },
    "bottle": {
      "name": "Empty Bottle",
      "aliases": ["(the +)?(empty +)?bottle"],
      "text": {
        "init_desc": "There is an empty bottle on a nearby table."
      },
      "visible": 1
    },
    "book": {
      "name": "Book",
      "aliases": ["the +book"],
      "text": {
        "init_desc": "On the bookshelf is a dusty book, entitled \"Magical Medicines of The Vista\".",
        "responses": {
          "read": "The book is entitled \"Magical Medicines of The Vista\". A particular page has been bookmarked. On this page, there is a riddle:\n\n\"In the woods, a magic flower\nof crimson colour and healing power\nSearch the dark, but note the way\nif you hope to see the light of day\""
        }
      },
      "visible": 1
    },
    "dingleflowers": {
      "name": "Dingleflowers",
      "aliases": ["(the +)?dingleflowers?", "(the +)?flowers?"],
      "text": {
        "init_desc": "Among them, you notice a small patch of crimson coloured Dingleflowers.",
        "responses": {}
      },
      "visible": 1
    },
    "axe": {
      "name": "Axe",
      "aliases": ["(the +)?(troll('?s)? +)?axe"],
      "text": {
        "init_desc": "The late troll's axe lies on the spot where it died.",
        "responses": {}
      },
      "visible": 0
    },
    "sapphire": {
      "name": "Blue Orb",
      "aliases": ["(the +)?((sapphire|blue) +(colou?red +)?)?orb", "the +sapphire"],
      "text": {
        "init_desc": "In the grass is a gleaming, sapphire coloured orb.",
        "responses": {}
      },
      "visible": 0
    },
    "ruby": {
      "name": "Red Orb",
      "aliases": ["(the +)?((ruby|red) +(colou?red +)?)?orb", "the +ruby"],
      "text": {
        "init_desc": "Inside is a gleaming, ruby coloured orb.",
        "responses": {}
      },
      "visible": 0
    },
    "dot": {
      "name": "Dot",
      "aliases": ["the +dot"],
      "text": {
        "init_desc": "",
        "responses": {}
      },
      "visible": 1
    },
    "sticks": {
      "name": "Sticks",
      "aliases": ["(the +)?(fire)?wood", "(the +)?sticks?", "a +stick", "(some|one) +(of +the +)?sticks", "some +(of +the +)?(fire)?wood", "one +stick"],
      "text": {
        "init_desc": "There are some sticks on the floor here, which could be used as firewood.",
        "responses": {}
      },
      "visible": 1
    },
    "matchbook": {
      "name": "Matchbook",
      "aliases": ["the +matchbook", "(the +)?matches"],
      "text": {
        "init_desc": "On the floor is a matchbook containing several matches.",
        "responses": {}
      },
      "visible": 0
    },
    "snow boots": {
      "name": "Snow Boots",
      "aliases": ["(the +)?(snow *)?boots"],
      "text": {
        "init_desc": "Inside is a pair of knackered old snow boots.",
        "responses": {}
      },
      "visible": 0
    },
    "hammer": {
      "name": "Hammer",
      "aliases": ["(the +)?hammer"],
      "text": {
        "init_desc": "The frost giant's hammer lies on the spot where it died.",
        "responses": {}
      },
      "visible": 0
    },
    "citrine": {
      "name": "Yellow Orb",
      "aliases": ["(the +)?((citrine|yellow) +(colou?red +)?)?orb", "the +citrine"],
      "text": {
        "init_desc": "In the snow is a gleaming, yellow coloured citrine... the yellow orb.",
        "responses": {}
      },
      "visible": 0
    }
  },
  "enemies": {
    "wood4goblin": {
      "name": "goblin",
      "type": "goblin",
      "init_desc": "However, a nasty looking goblin blocks your way west.",
      "blocks": ["west"],
      "inventory": [],
      "death_text": [
        "Your last attack was too much for the goblin. It dies, immediately disappearing in a plume of black smoke.",
        "The goblin dies instantly. What a pussy. Its body disappears in a plume of black smoke."
      ]
    },
    "wood7goblin": {
      "name": "goblin",
      "type": "goblin",
      "init_desc": "There is a goblin blocking your path. It says \"Turn back now, or meet your doom! My master will slay all who oppose him!\"",
      "blocks": ["west"],
      "inventory": [],
      "death_text": [
        "Your last attack was too much for the goblin. It dies, immediately disappearing in a plume of black smoke.",
        "The goblin dies instantly. What a pussy. Its body disappears in a plume of black smoke."
      ]
    },
    "wood9troll": {
      "name": "troll",
      "type": "troll",
      "init_desc": "A mighty troll towers over you, blocking your path. It wields an enormous axe, and clearly means to use it to put an end to your quest.\n\nTroll: \"You've done well to make it this far, kid... but it ends now. There's nothing you can do for your friends in the village. Surrender now, and I'll make this quick!\"",
      "blocks": ["west"],
      "inventory": ["axe", "sapphire"],
      "death_text": ["The troll is overcome by your attack. It falls to the floor, and says:\n\n\"You fool. You'll never defeat us! My brothers in arms will raze this land to the ground!\"\n\nThe troll vanishes in a spectacular plume of black smoke. The smoke clears to reveal a gleaming, sapphire coloured orb, and the fallen troll's axe."]
    },
    "moua2wolf": {
      "name": "wolf",
      "type": "(winter *)?wolf",
      "init_desc": "Or at least, you would be able to go north, if it weren't for the vicious winter wolf blocking your way.",
      "blocks": ["north"],
      "inventory": [],
      "death_text": [
        "Your attack defeats the winter wolf, which then disappears in a plume of black smoke.",
        "The winter wolf is defeated. It emits a blood-curdling howl as it disappears in a plume of black smoke."
      ]
    },
    "moub3wolf": {
      "name": "wolf",
      "type": "(winter *)?wolf",
      "init_desc": "However, a winter wolf, with pointed teeth and razor sharp claws, is blocking your way back.",
      "blocks": ["west"],
      "inventory": ["matchbook"],
      "death_text": [
        "Your attack defeats the winter wolf, which then disappears in a plume of black smoke.",
        "The winter wolf is defeated. It emits a blood-curdling howl as it disappears in a plume of black smoke."
      ]
    },
    "mouc2giant": {
      "name": "giant",
      "type": "(frost *)?giant",
      "init_desc": "Luckily, it won't go to waste. A huge frost giant stands here, blocking your way north. Adapted to winter environments, it has white skin, blue hair and eyes, and seems completely indifferent to the freezing temperature. It is dressed only in skins and some armour, but, more notably, carries a great hammer, which looks like it could do a tremendous amount of damage.",
      "blocks": ["north"],
      "inventory": ["hammer", "citrine"],
      "death_text": ["The frost giant is defeated. It falls to its knees, and says:\n\n\"How? How did this kid defeat us? Curse you, {name}!\"\n\nThe giant then vanishes in a great plume of smoke. Left behind, in the snow, is a yellow coloured orb of citrine, and the frost giant's hammer."]
    }
  },
  "starting_inventory": [],
  "ending": "Upon returning to the village, you see that everything is back to normal. Everyone is out celebrating in the streets, rejoicing in their new-found health. Jimbo and the Potion Master come rushing over to you.\n\nPotion Master: \"You did it, {name}! The curse is broken, and The Vista is saved! Thank you!\"\n\nJimbo: \"Yeah, nice job, buddy! I can't believe you got to save the world without me! You're the town hero! Everyone's been talking about all the adventures you went on. Did you really take down a frost giant?? You have to tell me everything!\"\n\n{name}: \"Alright guys, calm down. Don't break an arm jerking me off. Let's go get a pint.\"\n\nThe credits begin to roll, accompanied by a montage of you all getting smashed at Floonyloon Tavern."
}
