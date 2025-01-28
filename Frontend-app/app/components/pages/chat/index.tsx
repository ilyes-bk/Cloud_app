import dayjs from "dayjs";
import { useState } from "react";
import LeftSide from "./LeftSide";
import RightSide from "./RightSide";
import { conversations } from "~/lib/data/conversations.json";

export type Convo = ChatUser["messages"][number];
export type ChatUser = (typeof conversations)[number];

export default function ChatPage() {
  const [selectedUser, setSelectedUser] = useState<ChatUser>(conversations[0]);
  const [mobileSelectedUser, setMobileSelectedUser] = useState<ChatUser | null>(
    null
  );

  const currentMessage = selectedUser.messages.reduce(
    (acc: Record<string, Convo[]>, obj) => {
      const key = dayjs(obj.timestamp).format("D MMM, YYYY");

      // Create an array for the category if it doesn't exist
      if (!acc[key]) {
        acc[key] = [];
      }

      // Push the current object to the array
      acc[key].push(obj);

      return acc;
    },
    {}
  );
  return (
    <section className="flex h-full gap-2 overflow-hidden">
      {/* Left Side */}
      <LeftSide
        selectedUser={selectedUser}
        setSelectedUser={setSelectedUser}
        setMobileSelectedUser={setMobileSelectedUser}
      />

      {/* Right Side */}
      <RightSide
        currentMessage={currentMessage}
        selectedUser={selectedUser}
        mobileSelectedUser={mobileSelectedUser}
        setMobileSelectedUser={setMobileSelectedUser}
      />
    </section>
  );
}
