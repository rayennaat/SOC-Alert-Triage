package com.secuiq.backend.controllers;

import com.secuiq.backend.dto.predict.PredictRequest;
import com.secuiq.backend.dto.predict.PredictResponse;
import com.secuiq.backend.services.PredictService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/predict")
@RequiredArgsConstructor
@Tag(name = "Prediction", description = "ML-based alert severity prediction")
public class PredictController {

    private final PredictService predictService;

    @PostMapping
    @Operation(summary = "Predict alert severity", description = "Receives raw alert data and returns predicted severity + confidence score")
    @ApiResponse(responseCode = "200", description = "Prediction successful", content = @Content(schema = @Schema(implementation = PredictResponse.class)))
    @ApiResponse(responseCode = "400", description = "Invalid request format")
    @ApiResponse(responseCode = "500", description = "Prediction model error")
    public ResponseEntity<PredictResponse> predict(@RequestBody PredictRequest request) {
        PredictResponse response = predictService.predict(request);
        return ResponseEntity.ok(response);
    }
}