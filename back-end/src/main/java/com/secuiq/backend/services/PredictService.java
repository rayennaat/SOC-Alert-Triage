package com.secuiq.backend.services;

import com.secuiq.backend.dto.predict.PredictRequest;
import com.secuiq.backend.dto.predict.PredictResponse;

public interface PredictService {
    PredictResponse predict(PredictRequest request);
}