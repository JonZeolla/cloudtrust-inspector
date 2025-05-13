export enum EvidenceStatus {
    PENDING = "pending",
    APPROVED = "approved",
    REJECTED = "rejected",
    EXPIRED = "expired",
}

export enum EvidenceType {
    DOCUMENT = "document",
    SCREENSHOT = "screenshot",
    LOG = "log",
    CONFIGURATION = "configuration",
    TEST_RESULT = "test_result",
    OTHER = "other",
}

export interface Evidence {
    id: number
    title: string
    description: string
    evidence_type: EvidenceType
    status: EvidenceStatus
    control_id: number
    control_title: string
    file_url?: string
    created_at: string
    updated_at: string
    created_by: string
    updated_by: string
}

export interface EvidenceListResponse {
    items: Evidence[]
    total: number
    page: number
    pages: number
} 