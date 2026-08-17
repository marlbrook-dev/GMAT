export interface DropdownProps{label:string;items:Array<string|{value:string;label:string}>;onSelect?:(value:string)=>void;align?:'left'|'right';}
