import RightSideHeader from "../chat/Header";
import { useState } from "react";
import RightSideInputForm from "../chat/RightSideInputForm";
interface NewChatProps {
  onNewChat: (msg: string) => void;
}

export default function NewChat({ onNewChat }: NewChatProps) {
  const [inputText, setInputText] = useState("");

  return (
    <div className="flex flex-col w-full min-h-screen ">
      <RightSideHeader />
      <main className="flex-1 overflow-auto items-center justify-center flex">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-4">
              How can I help you today?
            </h2>
            <p className="text-xl text-gray-400 mb-8">
              I'm an AI assistant created to help you with various tasks. Feel
              free to ask me anything!
            </p>
            <div className="relative">
              <RightSideInputForm onSendMessage={onNewChat} />
              {/** 
              <Button onClick={onNewChat} size="lg">
                <Edit className="h-5 w-5 mr-2" />
                <span className="">Create new chat</span>
              </Button>
              */}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
