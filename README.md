<img src="https://u.til.pm/2023/07/amesu.png" alt="Art of the character 'Ameth' from Princess Connect! Re:Dive" align="right"/>

# `ameth`

> emeth (adverb, Hebrew) - firmness, faithfulness, truth

Authentication/recruitment vessel for the [PriConne Mapping](https://pcr.til.pm) project.

## Development

You will need `poetry` to deal with dependencies. Running `poetry install` in the project folder should take care of everything.

Create an *osu!* OAuth application. This can be done in your account settings. Make sure to add `http://localhost:5000/authorize` as a redirect URL.

Copy `.env.example` to `.env` and fill in your client ID & secret; you will also need a secret key for the session cookies.

Development secret keys typically don't need to be secure - but generating one is good practice anyway:
> `python -c "from secrets import token_hex; print(token_hex(24))"`

If everything is setup right, `poetry run flask run` should work!

## License

Apache 2
