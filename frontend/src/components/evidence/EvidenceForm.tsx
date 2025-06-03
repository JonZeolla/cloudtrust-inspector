import { useState } from "react"
import { useForm, Controller } from "react-hook-form"
import { useMutation } from "@tanstack/react-query"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { toast } from "sonner"
import { Evidence, EvidenceType } from "@/types/evidence"
import { api } from "@/lib/api"
import { zodResolver } from "@hookform/resolvers/zod"
import { formSchema } from "@/lib/validations/evidence"

interface EvidenceFormProps {
    onSuccess?: () => void
    initialData?: Partial<Evidence>
}

interface FormData {
    title: string
    description: string
    control_id: number
    evidence_type: EvidenceType
    file?: File
}

export function EvidenceForm({ onSuccess, initialData }: EvidenceFormProps) {
    const [file, setFile] = useState<File | null>(null)
    
    const { handleSubmit, control } = useForm<FormData>({
        defaultValues: initialData,
        resolver: zodResolver(formSchema),
    })

    const createEvidence = useMutation({
        mutationFn: async (data: FormData) => {
            const formData = new FormData()
            formData.append("title", data.title)
            formData.append("description", data.description)
            formData.append("control_id", data.control_id.toString())
            formData.append("evidence_type", data.evidence_type)
            if (file) {
                formData.append("file", file)
            }
            const response = await api.post("/evidence", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            })
            return response.data
        },
        onSuccess: () => {
            toast.success("Evidence created successfully")
            onSuccess?.()
        },
        onError: () => {
            toast.error("Failed to create evidence")
        }
    })

    const updateEvidence = useMutation({
        mutationFn: async (data: FormData) => {
            const formData = new FormData()
            formData.append("title", data.title)
            formData.append("description", data.description)
            formData.append("control_id", data.control_id.toString())
            formData.append("evidence_type", data.evidence_type)
            if (file) {
                formData.append("file", file)
            }
            const response = await api.put(`/evidence/${initialData?.id}`, formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            })
            return response.data
        },
        onSuccess: () => {
            toast.success("Evidence updated successfully")
            onSuccess?.()
        },
        onError: () => {
            toast.error("Failed to update evidence")
        }
    })

    const onSubmit = (data: FormData) => {
        if (initialData?.id) {
            updateEvidence.mutate(data)
        } else {
            createEvidence.mutate(data)
        }
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="space-y-2">
                <label htmlFor="title" className="text-sm font-medium">
                    Title
                </label>
                <Controller
                    name="title"
                    control={control}
                    rules={{ required: "Title is required" }}
                    render={({ field, fieldState }) => (
                        <>
                            <Input
                                id="title"
                                {...field}
                                className={fieldState.error ? "border-red-500" : ""}
                            />
                            {fieldState.error && (
                                <p className="text-sm text-red-500">{fieldState.error.message}</p>
                            )}
                        </>
                    )}
                />
            </div>

            <div className="space-y-2">
                <label htmlFor="description" className="text-sm font-medium">
                    Description
                </label>
                <Controller
                    name="description"
                    control={control}
                    render={({ field, fieldState }) => (
                        <>
                            <Textarea
                                id="description"
                                {...field}
                                className={fieldState.error ? "border-red-500" : ""}
                            />
                            {fieldState.error && (
                                <p className="text-sm text-red-500">{fieldState.error.message}</p>
                            )}
                        </>
                    )}
                />
            </div>

            <div className="space-y-2">
                <label htmlFor="evidence_type" className="text-sm font-medium">
                    Evidence Type
                </label>
                <Controller
                    name="evidence_type"
                    control={control}
                    rules={{ required: "Evidence type is required" }}
                    render={({ field, fieldState }) => (
                        <>
                            <Select
                                value={field.value}
                                onValueChange={field.onChange}
                            >
                                <SelectTrigger className={fieldState.error ? "border-red-500" : ""}>
                                    <SelectValue placeholder="Select evidence type" />
                                </SelectTrigger>
                                <SelectContent>
                                    {Object.values(EvidenceType).map((type) => (
                                        <SelectItem key={type} value={type}>
                                            {type.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            {fieldState.error && (
                                <p className="text-sm text-red-500">{fieldState.error.message}</p>
                            )}
                        </>
                    )}
                />
            </div>

            <div className="space-y-2">
                <label htmlFor="file" className="text-sm font-medium">
                    File
                </label>
                <Controller
                    name="file"
                    control={control}
                    render={({ field: { value, onChange, ...field }, fieldState }) => (
                        <>
                            <Input
                                id="file"
                                type="file"
                                onChange={(e) => {
                                    const file = e.target.files?.[0]
                                    if (file) {
                                        setFile(file)
                                        onChange(file)
                                    }
                                }}
                                className={fieldState.error ? "border-red-500" : ""}
                                {...field}
                            />
                            {fieldState.error && (
                                <p className="text-sm text-red-500">{fieldState.error.message}</p>
                            )}
                        </>
                    )}
                />
            </div>

            <Button
                type="submit"
                disabled={createEvidence.isPending || updateEvidence.isPending}
            >
                {createEvidence.isPending || updateEvidence.isPending
                    ? "Saving..."
                    : initialData?.id
                    ? "Update Evidence"
                    : "Create Evidence"}
            </Button>
        </form>
    )
} 