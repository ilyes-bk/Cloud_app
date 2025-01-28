import { ChevronDown, Check } from "lucide-react";
import { Button } from "~/components/custom/Button";
import { modelOptions } from "~/lib/data/ModelOptions";
import { cn } from "~/lib/utils";
import { useConversations } from "~/contexts/ConversationContext";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "~/components/ui/popover";
export const ModelSelect = () => {
  const {model, setModel} = useConversations()
  return (
    <Popover>
      <PopoverTrigger className="flex items-center rounded-lg px-3 py-2 text-base transition-all hover:bg-primary hover:text-primary-foreground">
        {model.label} <ChevronDown size={13} className="ml-1" />
      </PopoverTrigger>

      <PopoverContent
        className="mt-3 w-[320px] border bg-background p-1.5"
        sideOffset={5}
        align="start"
      >
        <ul className="w-full flex flex-col gap-3">
          {modelOptions.map((m, i) => {
            const { label, value, icon: Icon, description } = m;
            const selected = value === model.value;
            return (
              <li key={`${value}-${i}`} onClick={() => setModel(m)}>
                <Button className="flex group h-full w-full items-center justify-between whitespace-normal rounded-lg border border-transparent bg-transparent px-3 py-2 transition-all hover:cursor-pointer ">
                  <div className="flex items-center text-left text-primary group-hover:text-primary-foreground duration-75">
                    <Icon size={20} className="mr-2 shrink-0 " />

                    <div>
                      <div className="text-sm">{label}</div>
                      <div className="text-sm text-gray-400">{description}</div>
                    </div>
                  </div>

                  <div
                    className={cn(
                      "flex items-center justify-center w-4 h-4 border border-gray-400 rounded-full ml-3 shrink-0",
                      {
                        "bg-primary border-transparent group-hover:bg-white":
                          selected,
                      }
                    )}
                  >
                    {selected && (
                      <Check
                        size={10}
                        className="text-background group-hover:text-primary"
                        strokeWidth={4}
                      />
                    )}
                  </div>
                </Button>
              </li>
            );
          })}
        </ul>
      </PopoverContent>
    </Popover>
  );
};
