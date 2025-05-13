import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useState } from "react"

export function Settings() {
  const [currentPassword, setCurrentPassword] = useState("")
  const [newPassword, setNewPassword] = useState("")
  const [notifications, setNotifications] = useState(true)

  return (
    <div className="container mx-auto py-10 px-4 md:px-8 max-w-2xl">
      <div className="mb-8">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-2">Settings</h1>
        <p className="text-lg text-muted-foreground max-w-2xl">Manage your account, password, and notification preferences.</p>
      </div>
      <Card className="p-6 shadow-lg">
        <CardHeader>
          <CardTitle className="text-xl font-bold">Account Settings</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="current-password">Current Password</label>
              <Input id="current-password" type="password" value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="new-password">New Password</label>
              <Input id="new-password" type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} />
            </div>
            <Button type="submit" className="w-full" disabled>Change Password</Button>
            <div className="flex items-center gap-2 mt-6">
              <input id="notifications" type="checkbox" checked={notifications} onChange={e => setNotifications(e.target.checked)} className="accent-primary h-4 w-4 rounded" />
              <label htmlFor="notifications" className="text-sm">Enable email notifications</label>
            </div>
            <Button type="button" className="w-full" disabled>Save Preferences</Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
} 