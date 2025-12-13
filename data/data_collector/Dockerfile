FROM openjdk:17.0.2-jdk

WORKDIR /data_collector

COPY target/*.jar data_collector.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/data_collector/data_collector.jar"]