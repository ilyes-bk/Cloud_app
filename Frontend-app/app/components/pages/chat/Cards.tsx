import { Avatar, AvatarImage, AvatarFallback } from "~/components/ui/avatar";
import { Message } from "~/types/chat";
import React from "react";
import ReactMarkdown from "react-markdown";
import { Copy, CheckCheck, XCircle } from "lucide-react";
import { useState } from "react";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import { preprocessLaTeX } from "~/lib/processLatex";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import ToolCall from "./ToolCall";
import { AICard, HumanCard } from "./HumanCard";
interface ChatCardProps {
  indexIsLast: boolean;
  message: Message;
  lastMessageRef: React.RefObject<HTMLDivElement>;
  type?: string;
  imageUrl?: string;
  messages: any;
}
const AIURL = "/logo.png";
const MessageAvatar = ({ url }: any) => {
  return (
    <>
      <Avatar>
        <AvatarImage src={url} alt="user-avatar" />
        <AvatarFallback>AI</AvatarFallback>
      </Avatar>
    </>
  );
};

const ChatCard: React.FC<ChatCardProps> = React.memo(
  ({ message, indexIsLast, lastMessageRef, messages }) => {
    if (message.type == "human") {
      return (
        <HumanCard
          message={message}
          indexIsLast={indexIsLast}
          lastMessageRef={lastMessageRef}
        />
      );
    } else if (message?.tool_calls?.length == 0 && message.type == "ai") {
      return (
        <AICard
          message={message}
          indexIsLast={indexIsLast}
          lastMessageRef={lastMessageRef}
        />
      );
    } else if (message?.tool_calls?.length !== 0) {
      return message?.tool_calls.map((tool_call) => (
        <ToolCall key={tool_call.id} call={tool_call} messages={messages} />
      ));
    }
  }
);

export default ChatCard;
