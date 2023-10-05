FROM registry.gitlab.com/empaia/integration/ci-docker-images/test-runner:0.1.74@sha256:1de4ef90546b19bc6bd8bd0fbd116fe952ed4e5b7a5e8d61fd81bef491146e56 AS build0

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY isyntax_backend /isyntax/isyntax_backend
COPY pyproject.toml /isyntax/pyproject.toml

WORKDIR /isyntax

RUN python3 -m venv .venv
RUN poetry build

FROM ubuntu:18.04@sha256:152dc042452c496007f07ca9127571cb9c29697f42acbfad72324b2bb2e43c98

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y python3-pip python3-wheel unzip

COPY philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip /isyntax/philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip

WORKDIR /isyntax

RUN unzip philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip \
    && cd philips-pathologysdk-2.0-ubuntu18_04_py36_research \
    && chmod 777 InstallPathologySDK.sh \
    && ./InstallPathologySDK.sh py3 -y \
    && cd .. \
    && rm -r philips-pathologysdk-2.0-ubuntu18_04_py36_research

COPY --from=build0 /isyntax/dist/*.whl /tmp
RUN pip3 install /tmp/*.whl

RUN mkdir /data

CMD ["python3", "-m", "isyntax_backend"]
