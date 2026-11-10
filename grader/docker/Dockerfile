# Grader image: the simulator, the tool server and the final scorer.
#
# Build from the grader/ folder:   docker build -t pdgrader -f docker/Dockerfile .
#
# The build downloads the Minecraft server jar from Mojang. Building this image means you
# accept the Minecraft EULA (https://aka.ms/MinecraftEULA). Do not publish the built image:
# it contains Mojang's jar, which may not be redistributed.
FROM eclipse-temurin:25-jdk

RUN apt-get update && apt-get install -y --no-install-recommends python3 curl \
    && rm -rf /var/lib/apt/lists/*

ARG SERVER_JAR_URL=https://piston-data.mojang.com/v1/objects/33680f5f2ac32864d6d7cf5e56a705fdb3e05f4c/server.jar
ARG SERVER_JAR_SHA1=33680f5f2ac32864d6d7cf5e56a705fdb3e05f4c
RUN curl -fsSL -o /opt/server.jar "$SERVER_JAR_URL" \
    && echo "$SERVER_JAR_SHA1  /opt/server.jar" | sha1sum -c -

WORKDIR /opt/pdgrader
COPY pdgrader/ pdgrader/
COPY kernel/src/ kernel/src/
COPY kit_template/ kit_template/
COPY fixtures/ fixtures/
COPY reference_designs/ reference_designs/
COPY tests/ tests/
RUN python3 -m pdgrader setup --java-home "$JAVA_HOME" --server-jar /opt/server.jar

# One container per agent run. Mount a volume at /var/pdgrader to keep the log; never mount
# it into the agent's container.
EXPOSE 8811
ENTRYPOINT ["python3", "-m", "pdgrader"]
CMD ["serve", "--n", "3", "--track", "seamless", "--port", "8811", "--host", "0.0.0.0", "--log", "/var/pdgrader/log.jsonl"]
