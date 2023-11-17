# GPT Action Builder

Welcome! You've stumbled upon the GPT Action Builder. It started as a proof of concept, with the grand idea of making it easy for anyone to **craft their custom GPT Agents that make function calls with NO CODE**. Unfortunately, this turned out to be a bit tougher than I hoped due to technological hurdles. This project is currently more of a "sketch" than a "masterpiece."

But the upside is that I've laid out some foundational bricks on the path and now I'm turning to you, the community, for a helping hand. This project is an open invite to fellow tinkerers to experiment, tweak, and hopefully push through the hurdles where the original run came up short.

I truly believe systems that empower agents to build other agents is the future. **I'd love to see if others can get a framework like this working.**

## Here's what it does (high level):
* GPT determines what the user wants their GPT to do
* The GPT would search a reverse engineered version of the Postman API for their [Public API Network](https://www.postman.com/explore) (essentially provides the agent with access to public Postman schemas)
* The GPT would thne fetch the `openapi.json` from a Postman collection `id` using your Postman API key
* The GPT would then remove uneccesary info, validate minimum requirements, find authentication information, and getting started guides.
* Finally, it would return the schema to the user where they could use it for a brand new GPT that they built.

*[Here's the GPT that is currently deployed](https://chat.openai.com/g/g-fttFaS2lR-gpts-action-builder)*

## Getting Started

1. Clone/fork the repo `git clone git@github.com:petterle-endeavors/openapi-retriever.git`
2. *Optional*: Reopen in the provided dev container. NOTE: Deployments do NOT currently work in a dev container due to a file system mounting problem that i didn't take the time to figure out
3. If you did NOT open in a dev container,run `npm install -g projen aws-cdk && curl -sSL https://install.python-poetry.org | python3 - && poetry shell`
4. Run `make install`
5. RUn `projen`

After that, you should be good to go with all the required dependencies

### To run locally:
Use uvicorn or if using vscode, you can use the included `launch.json`

### To deploy:
1. run `make docker-start`
3. Configure your aws CLI if not already ([instructions for installing aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), [instructions for AWS SSO CLI](https://docs.aws.amazon.com/cli/latest/userguide/sso-configure-profile-token.html))
4. run `cdk deploy --all --app "python app.py" --profile <profile_name_configured_in_prior_step>`
5. Grab your [Postman API Key](https://learning.postman.com/docs/developer/postman-api/authentication/) and create a secret called `postman_api_key` in aws in the same region you deployed to.
6. Locate the deployed lambda in the console and grab the function url

### To create the GPT:
1. Login and subscribe to OpenAI plus
2. Create a new GPT
3. Insert the system [prompt](https://github.com/petterle-endeavors/openapi-retriever/blob/main/GPT%20Prompt) located in this repo
4. Grab `openapi.json` from `{base_lambda_function_url_from_previous_step}/openapi.json` and copy it into the GPT as a function call definition
5. Publish the GPT


## Learnings and Roadblocks

Here are a few takeaways and a couple of head-scratchers that came up (as of 11/15/2023):

- **Huge Files are a Pain:** Turns out, GPTs aren't fans of big files. If you're thinking of dealing with large files, be prepared for a bit of a wrestle.

- **Sandbox Constraints:** The system is sandboxed, with no options for network requests. Meaning, any talks with the outside world have to be through function calls or chat stuff.

- **GPTs Can't Upload...Yet:** Tried testing an upload file endpoint, but no cigar. GPTs can download files, but apparently, there's no uploading files to endpoints. So, you won't see it in the schema (even though there's an endpoint for it), but it's a good space for experimenting.

- **Valid OpenAPI.json—Where Art Thou?** Seriously, finding reliable OpenAPI.json files can feel like a wild goose chase. Thought I could outsmart the system by reverse engineering the Postman Public API, but ended up wading through too many garbage schemas.

- **Friendly Heads-up:** If you happen to find a nice treasure trove of openapi.json files, that'd be like hitting a gold mine. Or hey, you may want to give Zapier's API a whirl (although it's still in beta). Is Postman sitting on a gold mine here???

### Thinking Ahead

Honestly, I'm pretty excited about where this can go:

- **Handling Large Files:** Breaking through the large file hurdle with GPTs could be a great leap. And dare I say, uber cool?

- **Uploading Files:** File uploads stand as a challenge (not through the API, just those consumer-friendly GPTs). It's something that anyone cracking would kinda be a hero.

- **Better API Doc Sources:** This is a big one. Nailing down a quality source for API docs will be a game-changer. There's a potential business right there! Wonder if Postman knows they're potentially sitting on a gold mine...

Anyway, if you can help get this framework up and running, that'd be swell. And who knows, your contributions might just shape the future of GPTs and AI interaction.
