import { Metadata } from "next"

export const metadata: Metadata = {
    title: "Evidence Management",
    description: "Manage compliance evidence items",
}

export default function EvidenceLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return children
} 