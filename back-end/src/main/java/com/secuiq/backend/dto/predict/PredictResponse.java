package com.secuiq.backend.dto.predict;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data // Generates getters, setters, toString, equals, and hashCode methods or we can
      // replace with @Getter and @Setter
@AllArgsConstructor
@NoArgsConstructor
public class PredictResponse {
    private String alertId;
    private double priorityScore;
    private String modelVersion;
    private String explanation;
    private String timestamp;
}
