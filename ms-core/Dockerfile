# Build stage
FROM eclipse-temurin:21-jdk AS build
WORKDIR /home/app

COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
COPY src src

RUN ./mvnw install -DskipTests

# Package stage
FROM eclipse-temurin:21-jdk
WORKDIR /core
COPY --from=build /home/app/target/*.jar ms-core.jar
EXPOSE 8181
ENTRYPOINT ["java", "-jar", "ms-core.jar"]