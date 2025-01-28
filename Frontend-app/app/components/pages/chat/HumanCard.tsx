import { Avatar, AvatarImage, AvatarFallback } from "~/components/ui/avatar";
import ReactMarkdown from "react-markdown";
import { useState } from "react";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import rehypeKatex from "rehype-katex";
import { preprocessLaTeX } from "~/lib/processLatex";
import "katex/dist/katex.min.css";
import { Copy } from "lucide-react";
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

const HumanCard = ({ message, indexIsLast, lastMessageRef }: any) => {
  return (
    <div
      ref={indexIsLast ? lastMessageRef : null}
      className="flex items-start all-unset justify-end ml-4"
    >
      <div className="inline-block px-4 py-2 rounded-lg bg-gray-50 break-words text-black prose ">
        <ReactMarkdown>{message.content}</ReactMarkdown>
      </div>
      <MessageAvatar url="https://robohash.org/U1Y.png?set=set1" />
    </div>
  );
};

const AICard = ({ message, indexIsLast, lastMessageRef }:any) => {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(message.content).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000); // Reset after 2 seconds
    });
  };
  return (
    <div
      ref={indexIsLast ? lastMessageRef : null}
      className="flex items-start all-unset justify-start mr-8"
    >
      <>
        <MessageAvatar url={AIURL} />
        <div className="inline-block px-4 py-2 rounded-lg max-w-5xl bg-secondary text-secondary-foreground relative pr-8 prose">
          <ReactMarkdown
            remarkPlugins={[remarkGfm, remarkMath]}
            rehypePlugins={[rehypeKatex]}
          >
            {preprocessLaTeX(message.content)}
          </ReactMarkdown>
          <button
            onClick={handleCopy}
            className="absolute top-2 right-2 p-1 bg-secondary text-secondary-foreground hover:bg-opacity-80 rounded"
            aria-label="Copy to clipboard"
          >
            <Copy size={16} />
          </button>
          {copied && (
            <span className="absolute top-2 right-12 text-sm">Copied!</span>
          )}
        </div>
      </>
    </div>
  );
};

export {HumanCard, AICard}