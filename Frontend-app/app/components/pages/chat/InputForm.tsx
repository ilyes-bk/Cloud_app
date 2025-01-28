import { PaperclipIcon, SendIcon, Trash2 } from "lucide-react";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/custom/Button";
import { useState } from "react";

const RightSideInputForm: React.FC = () => {
  const [inputText, setInputText] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
  };
  return (
    <form
      className="relative flex w-full flex-none flex-col items-center gap-2"
      onSubmit={handleSubmit}
    >
      <div className="flex w-full items-center gap-2">
        <Input className="flex-1" placeholder="Type your message here..." />
        <Input
          type="file"
          id="file-upload"
          className="hidden"
        />
        <Button
          type="button"
          variant="outline"
          onClick={() => document.getElementById("file-upload")?.click()}
        >
          <PaperclipIcon className="h-4 w-4" />
          <span className="sr-only">Attach file</span>
        </Button>
        <Button type="submit">
          <SendIcon className="h-4 w-4" />
          <span className="sr-only">Send</span>
        </Button>
        <Button>
          <Trash2 className="h-4 w-4" />
          <span className="sr-only">Send</span>
        </Button>
      </div>
      {selectedFile && (
        <div className="mt-2 w-full text-sm text-gray-500">
          Selected file: {selectedFile.name}
        </div>
      )}
    </form>
  );
};

export default RightSideInputForm;
