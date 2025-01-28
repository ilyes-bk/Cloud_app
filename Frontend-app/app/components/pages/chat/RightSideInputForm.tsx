import React, { useRef, useState } from "react";
import { PaperclipIcon, SendIcon, Trash2 } from "lucide-react";
import { Button } from "~/components/custom/Button";
import RightSideInputFields from "./RightSideInputFields";
import { handleFileChange, resetFileInput } from "~/lib/helpers/FileHandler";
interface RightSideInputFormProps {
  onSendMessage: (message: string, imageData?: string) => void;
  onDelete?: () => void;
  showFile?: boolean;
}

const RightSideInputForm: React.FC<RightSideInputFormProps> = ({
  onSendMessage,
  onDelete,
  showFile
}) => {
  const [inputText, setInputText] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (inputText.trim() || selectedFile) {
      if (selectedFile && selectedFile.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const imageData = e.target?.result as string;
          onSendMessage(inputText, imageData);
          setInputText("");
          resetFileInput(fileInputRef, setSelectedFile);
        };
        reader.readAsDataURL(selectedFile);
      } else {
        onSendMessage(inputText);
        setInputText("");
        resetFileInput(fileInputRef, setSelectedFile);
      }
    }
  };
  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Detect if "Enter" key is pressed without "Shift" to submit
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();  // Prevent form submission via Enter key
      handleSubmit(e);  // Manually trigger submit when Enter is pressed
    }
  };
  return (
    <form
      className="flex w-full flex-none gap-2 relative items-center max-w-3xl m-auto"
      onSubmit={handleSubmit}
    >
      <RightSideInputFields inputText={inputText} setInputText={setInputText} onKeyDown={handleKeyDown} />
      <input
        type="file"
        ref={fileInputRef}
        onChange={(e) => handleFileChange(e, setSelectedFile)}
        className="hidden"
        id="file-input"
      />
      {showFile && (
        <Button
          disabled
          type="button"
          variant="outline"
          onClick={() => fileInputRef.current?.click()}
        >
          <PaperclipIcon className="h-4 w-4" />
          <span className="sr-only">Attach file</span>
        </Button>
      )}

      {onDelete && (
        <Button onClick={onDelete}>
          <Trash2 className="h-4 w-4" />
        </Button>
      )}

      <Button type="submit" disabled={!inputText && !selectedFile}>
        <SendIcon className="h-4 w-4" />
        <span className="sr-only">Send</span>
      </Button>
      {selectedFile && (
        <div className="absolute bottom-full left-0 mb-2 text-sm text-gray-500">
          Selected file: {selectedFile.name}
        </div>
      )}
    </form>
  );
};

export default RightSideInputForm;
