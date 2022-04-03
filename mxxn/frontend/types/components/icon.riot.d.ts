import { RiotComponent, RiotComponentWrapper } from 'riot';
interface Props {
    name: string;
}
interface State {
    isReady: boolean;
}
export interface Icon extends RiotComponent<Props, State> {
    change: (string: any) => void;
}
declare const _default: RiotComponentWrapper<Icon>;
export default _default;
