from __future__ import annotations

import uvicorn

from pythonprojecttemplate.config.settings import settings


def main() -> None:
    uvicorn.run(
        "pythonprojecttemplate.api.app:create_application",
        factory=True,
        host=settings.api.host,
        port=settings.api.port,
        reload=False,
    )


if __name__ == "__main__":
    main()

