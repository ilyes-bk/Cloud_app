import React, { useEffect, useRef, useState } from "react";
import { ScrollArea } from "~/components/ui/scroll-area";
import ChatCard from "./Cards";
import { Message } from "~/types/chat";
import GenCard from "./GenCard";
import ConfirmationCard from "./ConfirmCard";
interface ChatAreaProps {
  conversation: any;
  generating: any;
  chunks: any;
  confirmation: string | undefined;
}

const ChatArea: React.FC<ChatAreaProps> = ({
  conversation,
  generating,
  chunks,
  confirmation
}) => {
  const scrollViewportRef = useRef<HTMLDivElement>(null);
  const lastMessageRef = useRef<HTMLDivElement>(null);
  const loadingMessageRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollViewportRef.current) {
      const scrollToElement = (element: HTMLElement) => {
        element.scrollIntoView({ behavior: "smooth", block: "end" });
      };

      if (loadingMessageRef.current) {
        requestAnimationFrame(() =>
          scrollToElement(loadingMessageRef.current!)
        );
      } else if (lastMessageRef.current) {
        requestAnimationFrame(() => scrollToElement(lastMessageRef.current!));
      }
    }
  }, [conversation]);

  return (
    <ScrollArea className="flex-1">
      <div
        ref={scrollViewportRef}
        className="p-4 mb-10 max-w-5xl m-auto flex flex-col gap-4"
      >

        {conversation?.messages &&
          conversation?.messages.map(
            (message: Message, index: number) =>(
              (message.type == "ai" ||
              message.type == "human") && (
                <ChatCard
                  key={message.id}
                  messages={conversation?.messages}
                  indexIsLast={index === conversation?.messages.length - 1}
                  lastMessageRef={lastMessageRef}
                  message={message}
                />
              ))
          )}
        <ConfirmationCard confirmation={confirmation} />
        <GenCard generating={generating} message={chunks} />
      </div>
    </ScrollArea>
  );
};

export default ChatArea;
