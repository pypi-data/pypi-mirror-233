FROM nyamisty/docker-wine-dotnet as pre-build

COPY . /slide_access

RUN unzip -qq /slide_access/mirax_backend.zip -d /slide_access/mirax_backend

FROM nyamisty/docker-wine-dotnet as build

RUN export WINEARCH=win32; export WINEPREFIX=$(realpath ~/.wine32) winecfg

RUN mkdir /slide_access
COPY --from=pre-build /slide_access /slide_access

RUN find ./slide_access/mirax_backend/ -type f -name "ipp*.dll" | xargs -i mv {} ~/.wine/drive_c/windows/system32/
RUN mv /slide_access/mirax_backend/libiomp5md.dll ~/.wine/drive_c/windows/system32/

RUN mkdir /slide_access/slideac_x86
RUN mv /slide_access/mirax_backend/SlideIO.dll /slide_access/slideac_x86
RUN mv /slide_access/mirax_backend/ImgCodecs.dll /slide_access/slideac_x86
RUN mv /slide_access/mirax_backend/SlideAC.dll /slide_access/slideac_x86

RUN wine regedit /slide_access/mirax_backend/SlideAC.reg && sleep 5

RUN wine regsvr32.exe /slide_access/slideac_x86/SlideIO.dll && sleep 2
RUN wine regsvr32.exe /slide_access/slideac_x86/ImgCodecs.dll && sleep 2
RUN wine regsvr32.exe /slide_access/slideac_x86/SlideAC.dll && sleep 2

RUN chmod gou+x /slide_access/entrypoint.sh

CMD ["/slide_access/entrypoint.sh"]