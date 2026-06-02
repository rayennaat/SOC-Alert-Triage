package com.secuiq.backend.dto.alerts;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Schema(description = "Paginated list of alerts")
public class AlertListResponse {

    @NotBlank
    @Schema(description = "List of alerts on the current page")
    private java.util.List<AlertResponse> items;

    @NotBlank
    @Schema(example = "0")
    private int page;

    @NotBlank
    @Schema(example = "10")
    private int size;

    @NotBlank
    @Schema(example = "100")
    private long totalElements;

    @NotBlank
    @Schema(example = "5")
    private int totalPages;

    public java.util.List<AlertResponse> getItems() {
        return items;
    }

    public void setItems(java.util.List<AlertResponse> items) {
        this.items = items;
    }

    public int getPage() {
        return page;
    }

    public void setPage(int page) {
        this.page = page;
    }

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
    }

    public long getTotalElements() {
        return totalElements;
    }

    public void setTotalElements(long totalElements) {
        this.totalElements = totalElements;
    }

    public int getTotalPages() {
        return totalPages;
    }

    public void setTotalPages(int totalPages) {
        this.totalPages = totalPages;
    }
}
