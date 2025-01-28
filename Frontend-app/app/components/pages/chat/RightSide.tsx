import ChatArea from "./ChatArea";
import RightSideInputForm from "./RightSideInputForm";
import RightSideHeader from "./Header";
import useConversation from "~/lib/useConversation";
import { useLoaderData } from "@remix-run/react";

const RightSide = () => {
  const initialConversation:any = useLoaderData()
  const {conversation, onSendMessage, onDelete, chunks, generating, confirmation} = useConversation(initialConversation)
  return (
    <div className="flex flex-col flex-grow p-4">
      <RightSideHeader />
      <ChatArea conversation={conversation} generating={generating} chunks={chunks} confirmation={confirmation}/>
      <RightSideInputForm onDelete={onDelete} onSendMessage={onSendMessage} />
    </div>
  );
};

export default RightSide;
