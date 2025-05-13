import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { format as formatDate } from "date-fns"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Badge } from "@/components/ui/badge"
import { toast } from "sonner"
import { MoreHorizontal, FileText, Download, Trash2, CheckCircle2, XCircle, Clock } from "lucide-react"
import { EvidenceStatus, Evidence } from "@/types/evidence"
import { api } from "@/lib/api"

export function EvidenceList() {
    const queryClient = useQueryClient()
    const [selectedStatus, setSelectedStatus] = useState<EvidenceStatus | "all">("all")
    const [page, setPage] = useState(1)
    const pageSize = 10

    const { data, isLoading, error } = useQuery({
        queryKey: ["evidence", selectedStatus],
        queryFn: async () => {
            const params = new URLSearchParams()
            if (selectedStatus !== "all") {
                params.append("status", selectedStatus)
            }
            const response = await api.get(`/evidence?${params.toString()}`)
            return response.data
        }
    })

    const deleteEvidence = useMutation({
        mutationFn: async (id: number) => {
            await api.delete(`/evidence/${id}`)
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["evidence"] })
            toast.success("Evidence deleted successfully")
        },
        onError: () => {
            toast.error("Failed to delete evidence")
        }
    })

    const updateStatus = useMutation({
        mutationFn: async ({ id, status }: { id: number; status: EvidenceStatus }) => {
            await api.put(`/evidence/${id}/status`, { status })
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["evidence"] })
            toast.success("Evidence status updated successfully")
        },
        onError: () => {
            toast.error("Failed to update evidence status")
        }
    })

    const handleDownload = (format: "html" | "pdf") => {
        const timestamp = formatDate(new Date(), "yyyyMMdd_HHmmss")
        const link = document.createElement("a")
        link.href = `/api/reports/download?format=${format}`
        link.setAttribute("download", `compliance_report_${timestamp}.${format}`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }

    if (isLoading) {
        return <div>Loading...</div>
    }

    if (error) {
        return <div>Error loading evidence items. Please try again.</div>
    }

    const getStatusBadge = (status: EvidenceStatus) => {
        const variants = {
            [EvidenceStatus.APPROVED]: "success",
            [EvidenceStatus.PENDING]: "warning",
            [EvidenceStatus.REJECTED]: "destructive",
            [EvidenceStatus.EXPIRED]: "secondary",
        } as const

        const icons = {
            [EvidenceStatus.APPROVED]: <CheckCircle2 className="w-4 h-4" />,
            [EvidenceStatus.PENDING]: <Clock className="w-4 h-4" />,
            [EvidenceStatus.REJECTED]: <XCircle className="w-4 h-4" />,
            [EvidenceStatus.EXPIRED]: <Clock className="w-4 h-4" />,
        }

        return (
            <Badge variant={variants[status]} className="flex items-center gap-1">
                {icons[status]}
                {status.charAt(0).toUpperCase() + status.slice(1)}
            </Badge>
        )
    }

    // Mock evidence data for demo
    const mockEvidence = [
        {
            id: 1,
            title: "IAM Policy Review",
            control_title: "NIST-AC-1",
            evidence_type: "document",
            status: "approved",
            created_at: "2024-06-01T10:00:00Z",
            updated_at: "2024-06-01T10:00:00Z",
        },
        {
            id: 2,
            title: "S3 Bucket Encryption",
            control_title: "NIST-SC-13",
            evidence_type: "screenshot",
            status: "approved",
            created_at: "2024-06-02T11:00:00Z",
            updated_at: "2024-06-02T11:00:00Z",
        },
        {
            id: 3,
            title: "CloudTrail Enabled",
            control_title: "NIST-AU-2",
            evidence_type: "log",
            status: "approved",
            created_at: "2024-06-03T12:00:00Z",
            updated_at: "2024-06-03T12:00:00Z",
        },
        {
            id: 4,
            title: "MFA Enforcement",
            control_title: "NIST-IA-2",
            evidence_type: "document",
            status: "pending",
            created_at: "2024-06-04T13:00:00Z",
            updated_at: "2024-06-04T13:00:00Z",
        },
        {
            id: 5,
            title: "Security Group Review",
            control_title: "NIST-AC-4",
            evidence_type: "log",
            status: "rejected",
            created_at: "2024-06-05T14:00:00Z",
            updated_at: "2024-06-05T14:00:00Z",
        },
        {
            id: 6,
            title: "VPC Flow Logs",
            control_title: "NIST-AU-12",
            evidence_type: "log",
            status: "approved",
            created_at: "2024-06-06T15:00:00Z",
            updated_at: "2024-06-06T15:00:00Z",
        },
        {
            id: 7,
            title: "Password Policy",
            control_title: "NIST-IA-5",
            evidence_type: "document",
            status: "pending",
            created_at: "2024-06-07T16:00:00Z",
            updated_at: "2024-06-07T16:00:00Z",
        },
        {
            id: 8,
            title: "KMS Key Rotation",
            control_title: "NIST-SC-12",
            evidence_type: "log",
            status: "approved",
            created_at: "2024-06-08T17:00:00Z",
            updated_at: "2024-06-08T17:00:00Z",
        },
    ]

    // Use mock data if no data from backend
    const evidenceItems = data?.items && data.items.length > 0 ? data.items : mockEvidence

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold tracking-tight">Evidence Items</h2>
                <div className="flex gap-2">
                    <Button
                        variant={selectedStatus === "all" ? "default" : "outline"}
                        onClick={() => setSelectedStatus("all")}
                    >
                        All
                    </Button>
                    {Object.values(EvidenceStatus).map((status) => (
                        <Button
                            key={status}
                            variant={selectedStatus === status ? "default" : "outline"}
                            onClick={() => setSelectedStatus(status)}
                        >
                            {status.replace(/_/g, " ").replace(/\b\w/g, (l: string) => l.toUpperCase())}
                        </Button>
                    ))}
                    <Button
                        variant="outline"
                        onClick={() => handleDownload("html")}
                        className="flex items-center gap-2"
                    >
                        <FileText className="w-4 h-4" />
                        Export HTML
                    </Button>
                    <Button
                        variant="outline"
                        onClick={() => handleDownload("pdf")}
                        className="flex items-center gap-2"
                    >
                        <Download className="w-4 h-4" />
                        Export PDF
                    </Button>
                </div>
            </div>

            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Title</TableHead>
                            <TableHead>Control</TableHead>
                            <TableHead>Type</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Created</TableHead>
                            <TableHead>Updated</TableHead>
                            <TableHead className="w-[70px]"></TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {evidenceItems.map((item: Evidence) => (
                            <TableRow key={item.id}>
                                <TableCell className="font-medium">{item.title}</TableCell>
                                <TableCell>{item.control_title}</TableCell>
                                <TableCell>
                                    {item.evidence_type.replace(/_/g, " ").replace(/\b\w/g, (letter: string) => letter.toUpperCase())}
                                </TableCell>
                                <TableCell>{getStatusBadge(item.status)}</TableCell>
                                <TableCell>{formatDate(new Date(item.created_at), "MMM d, yyyy")}</TableCell>
                                <TableCell>{formatDate(new Date(item.updated_at), "MMM d, yyyy")}</TableCell>
                                <TableCell>
                                    <DropdownMenu>
                                        <DropdownMenuTrigger asChild>
                                            <Button variant="ghost" className="h-8 w-8 p-0">
                                                <span className="sr-only">Open menu</span>
                                                <MoreHorizontal className="h-4 w-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuLabel>Actions</DropdownMenuLabel>
                                            <DropdownMenuSeparator />
                                            {item.status !== EvidenceStatus.APPROVED && (
                                                <DropdownMenuItem
                                                    onClick={() =>
                                                        updateStatus.mutate({
                                                            id: item.id,
                                                            status: EvidenceStatus.APPROVED,
                                                        })
                                                    }
                                                >
                                                    <CheckCircle2 className="w-4 h-4 mr-2" />
                                                    Approve
                                                </DropdownMenuItem>
                                            )}
                                            {item.status !== EvidenceStatus.REJECTED && (
                                                <DropdownMenuItem
                                                    onClick={() =>
                                                        updateStatus.mutate({
                                                            id: item.id,
                                                            status: EvidenceStatus.REJECTED,
                                                        })
                                                    }
                                                >
                                                    <XCircle className="w-4 h-4 mr-2" />
                                                    Reject
                                                </DropdownMenuItem>
                                            )}
                                            <DropdownMenuSeparator />
                                            <DropdownMenuItem
                                                className="text-red-600"
                                                onClick={() => deleteEvidence.mutate(item.id)}
                                            >
                                                <Trash2 className="w-4 h-4 mr-2" />
                                                Delete
                                            </DropdownMenuItem>
                                        </DropdownMenuContent>
                                    </DropdownMenu>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>

            {data && data.total > 0 && (
                <div className="flex items-center justify-between">
                    <div className="text-sm text-muted-foreground">
                        Showing {((page - 1) * pageSize) + 1} to{" "}
                        {Math.min(page * pageSize, data.total)} of {data.total} items
                    </div>
                    <div className="flex gap-2">
                        <Button
                            variant="outline"
                            onClick={() => setPage(page - 1)}
                            disabled={page === 1}
                        >
                            Previous
                        </Button>
                        <Button
                            variant="outline"
                            onClick={() => setPage(page + 1)}
                            disabled={page >= data.pages}
                        >
                            Next
                        </Button>
                    </div>
                </div>
            )}
        </div>
    )
} 