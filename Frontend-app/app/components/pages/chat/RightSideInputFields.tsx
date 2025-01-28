import React from "react";
import { Input, useAutosizeTextArea } from "~/components/ui/input";
import { useRef } from "react";

interface RightSideInputFieldsProps {
  inputText: string;
  setInputText: (text: string) => void;
  onKeyDown?: (e: React.KeyboardEvent)=>void;
}

const RightSideInputFields: React.FC<RightSideInputFieldsProps> = ({
  inputText,
  setInputText,
  onKeyDown
}) => {

  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  useAutosizeTextArea(textAreaRef.current, inputText);

  return (
    <Input
      className="flex-1"
      placeholder="Type your message here..."
      value={inputText}
      onChange={(event) => setInputText(event.target.value)}
      onKeyDown={onKeyDown}

      ref={textAreaRef}
    />
  );
};

export default RightSideInputFields;
