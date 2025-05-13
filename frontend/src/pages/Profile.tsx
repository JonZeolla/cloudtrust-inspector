import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { useState } from "react"

export function Profile() {
  const [name, setName] = useState("CloudTrust User")
  const [email, setEmail] = useState("user@cloudtrust.inspector")
  const [avatar, setAvatar] = useState<string | undefined>(undefined)

  return (
    <div className="container mx-auto py-10 px-4 md:px-8 max-w-2xl">
      <div className="mb-8">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-2">Profile</h1>
        <p className="text-lg text-muted-foreground max-w-2xl">View and update your personal information and avatar.</p>
      </div>
      <Card className="p-6 flex flex-col items-center gap-6 shadow-lg">
        <CardHeader className="flex flex-col items-center gap-2">
          <Avatar className="h-20 w-20">
            {avatar ? (
              <AvatarImage src={avatar} alt={name} />
            ) : (
              <AvatarFallback>{name.split(" ").map(n => n[0]).join("")}</AvatarFallback>
            )}
          </Avatar>
          <CardTitle className="text-2xl font-bold mt-2">{name}</CardTitle>
          <p className="text-muted-foreground">{email}</p>
        </CardHeader>
        <CardContent className="w-full max-w-md">
          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="name">Name</label>
              <Input id="name" value={name} onChange={e => setName(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="email">Email</label>
              <Input id="email" type="email" value={email} onChange={e => setEmail(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="avatar">Avatar URL</label>
              <Input id="avatar" value={avatar || ""} onChange={e => setAvatar(e.target.value)} placeholder="https://..." />
            </div>
            <Button type="submit" className="w-full mt-4" disabled>Save Changes</Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
} 