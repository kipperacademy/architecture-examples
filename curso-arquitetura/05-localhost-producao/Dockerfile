FROM eclipse-temurin:21-jdk AS build
WORKDIR /build
COPY pratica/Servidor.java .
RUN javac -encoding UTF-8 -d out Servidor.java

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /build/out/ /app/
ENV HOST=0.0.0.0 PORT=8080 INSTANCE=container
USER 10001:10001
EXPOSE 8080
ENTRYPOINT ["java", "-cp", "/app", "Servidor"]
