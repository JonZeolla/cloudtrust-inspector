"use client"

import { EvidenceList } from "@/components/evidence/EvidenceList"
import { EvidenceForm } from "@/components/evidence/EvidenceForm"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"
import { useState } from "react"

export default function EvidencePage() {
    const [showForm, setShowForm] = useState(false)

    return (
        <div className="container mx-auto py-10">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Evidence Management</h1>
                    <p className="text-muted-foreground">
                        Manage and track compliance evidence items
                    </p>
                </div>
                <Button onClick={() => setShowForm(!showForm)}>
                    <Plus className="w-4 h-4 mr-2" />
                    {showForm ? "Hide Form" : "Add Evidence"}
                </Button>
            </div>

            {showForm && (
                <div className="mb-8 p-6 border rounded-lg bg-card">
                    <h2 className="text-xl font-semibold mb-4">Add New Evidence</h2>
                    <EvidenceForm onSuccess={() => setShowForm(false)} />
                </div>
            )}

            <EvidenceList />
        </div>
    )
} 