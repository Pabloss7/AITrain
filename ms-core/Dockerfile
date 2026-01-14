FROM eclipse-temurin:21-jdk

WORKDIR /core

COPY target/*.jar ms-core.jar

EXPOSE 8181

ENTRYPOINT ["java", "-jar", "ms-core.jar"]