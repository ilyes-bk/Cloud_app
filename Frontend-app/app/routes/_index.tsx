import { ActionFunction, type MetaFunction } from "@remix-run/node";
import LeftSide from "~/components/pages/chat/LeftSide";
import NewChat from "~/components/pages/emptyChat/NewChat";
import { useState } from "react";
import ChatArea from "~/components/pages/chat/ChatArea";
import RightSideInputForm from "~/components/pages/chat/RightSideInputForm";
import RightSideHeader from "~/components/pages/chat/Header";
import useConversation from "~/lib/useConversation";
export const meta: MetaFunction = () => {
  return [
    { title: "Chats" },
    { name: "description", content: "Chats" },
  ];
};

export default function Index() {
  const { conversation, onSendMessage, onDelete, chunks, generating } =
    useConversation(null);
  const [newConv, setNewConversation] = useState(false);

  return (
    <div className="h-screen flex">
      <LeftSide
        onCreateNewChat={() => {}}
      />
      {newConv ? (
        <div className="flex flex-col flex-grow p-4">
          <RightSideHeader />
          <ChatArea
            conversation={conversation}
            generating={generating}
            chunks={chunks}
          />
          <RightSideInputForm
            onDelete={onDelete}
            onSendMessage={onSendMessage}
          />
        </div>
      ) : (
        <NewChat
          onNewChat={(msg:string) => {
            onSendMessage(msg);
            setNewConversation(true);
          }}
        />
      )}
    </div>
  );
}
