# Build stage
FROM maven:3.8.5-openjdk-17 AS build
WORKDIR /home/app
COPY pom.xml .
COPY src src
RUN mvn clean package -DskipTests

# Package stage
FROM eclipse-temurin:17-jre
WORKDIR /data_collector
COPY --from=build /home/app/target/*.jar data_collector.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "data_collector.jar"]