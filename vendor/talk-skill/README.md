# Personal Note

Every AI conversation feels the same — robotic, overly polished, weirdly formal. You say something real and get back a five-paragraph essay starting with "That's a great question!" Nobody talks like that. I built this skill because I wanted conversations that actually feel like conversations. Where the AI matches your energy, picks up on what you're really saying, knows when to go deep and when to just chill. It's not perfect, but it's a step toward making AI feel less like a search engine and more like someone who actually gets you.

---

# Talk Skill

A Claude Desktop skill that transforms AI conversations from robotic assistant interactions into real, human-like exchanges. It reads subtext, matches your energy, finds deep meaning when the moment calls for it, and knows when to just shut up and listen.

## What It Does

When you invoke `/talk`, Claude stops being an assistant and starts being a conversation partner:

- **Matches your energy** — casual when you're casual, deep when you're deep, gentle when you need it
- **Reads between the lines** — picks up on what you're NOT saying, emotional undertones, and recurring themes
- **Finds deep meaning** — connects your words to bigger life themes, values, and patterns you might not see
- **Gives real consolation** — no hollow platitudes, no rushing to fix things, just genuine presence
- **Tells stories** — uses analogies, metaphors, and "this reminds me of..." moments instead of clinical explanations
- **Mirrors your humor** — detects if you're sarcastic, goofy, or dry and responds in kind
- **Pushes back** — real friends don't just agree with everything; this skill challenges you when it matters
- **Knows when to shut up** — sometimes "yeah, that's real" is the best response
- **Stays curious** — asks follow-ups like "wait, what happened after that?" instead of "could you elaborate?"

## Token Efficiency

This skill is designed to be **token-conscious**. It:

- Matches response length to your message length (no essays when a sentence will do)
- Cuts filler and signposting language
- Says things once instead of rephrasing three ways
- Automatically uses the lightest model tier appropriate for the conversation depth

You won't burn through your quota on casual chat.

## Installation

This skill is designed for **Claude Desktop (Cowork)**.

### Option 1: Save directly
Copy the contents of `SKILL.md` and save it as a skill named `talk` in your Claude Desktop app.

### Option 2: Manual install
1. Navigate to your Claude skills directory
2. Create a folder named `talk`
3. Place `SKILL.md` inside it

## Usage

```
/talk
```

That's it. No arguments needed. Just invoke it and start talking. Claude will shift into conversation mode naturally — no "Talk mode activated!" nonsense.

You can also start with a topic:

```
/talk I've been thinking about whether I'm in the right career
/talk honestly today was rough
/talk what's the most overrated thing everyone pretends to like
```

## What It Won't Do

- Won't psychoanalyze you — it's a conversation partner, not a therapist
- Won't agree with everything — yes-men are boring
- Won't force depth — sometimes a conversation is just a conversation
- Won't use emojis unless you do first
- Won't monologue — responses stay proportional to yours

## How It's Different From Default Claude

| Behavior | Default Claude | **With /talk** |
|----------|---------------|----------------|
| Greeting | "I'd be happy to help!" | *just starts naturally* |
| Response to venting | Bullet-pointed solutions | Sits with you first |
| Formatting | Headers, bold, lists | Natural flowing text |
| Disagreement | "There are many perspectives..." | "I don't think that's it though" |
| Humor | Safe, generic | Mirrors YOUR style |
| Response length | Often too long | Matches your energy |
| Follow-ups | "Could you elaborate?" | "Wait what happened after that?" |

## Requirements

- Claude Desktop app with Cowork enabled

## License

MIT License — see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! If you have ideas for making AI conversations feel more human, open an issue or PR. See [CONTRIBUTING.md](CONTRIBUTING.md).
