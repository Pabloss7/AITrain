FROM openjdk:17-jdk-slim

WORKDIR /data_collector

COPY target/*.jar data_collector.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/data_collector/data_collector.jar"]