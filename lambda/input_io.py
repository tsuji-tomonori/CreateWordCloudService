from typing import NamedTuple


class ChatItem(NamedTuple):
    # メタ情報
    meta_type: str  # メッセージタイプ
    meta_publishedat: str  # メッセージが最初に公開された日時 ISO8601
    # メッセージ情報
    message_text: str  # メッセージ
    message_channelid: str  # メッセージを作成したユーザーのID
    # 削除情報
    deleted_messageid: str  # 削除されたメッセージを一意に識別するID
    # 無料スパチャ情報
    member_usercomment: str  # コメント
    member_month: int  # メンバー合計月数(切り上げ)
    member_lebelname: str  # メンバーレベル名
    # 新規メンバー情報
    newsponsor_lebelname: str  # メンバーレベル名
    newsponsor_upgrade: bool  # アップグレードの有無 新規メンバーはfalse
    # スパチャ情報
    superchat_amountmicros: float  # 金額(マイクロ単位)
    superchat_currency: str  # 通貨(ISO4217)
    superchat_usercomment: str  # コメント
    superchat_tier: int  # 有料メッセージの階級
    # スーパーチケット情報
    supersticker_id: str  # ステッカーを一意に識別するID
    supersticker_alttext: str  # ステッカーを説明する文字列
    supersticker_amountmicros: float  # 金額(マイクロ単位)
    supersticker_currency: str  # 通貨(ISO4217)
    supersticker_tier: int  # 有料メッセージの階級
    # メンバーギフト情報(送る側)
    membergift_count: int  # ユーザーが購入したメンバーシップギフトの数
    membergift_lebelname: str  # 購入したメンバーシップギフトのレベル
    # メンバーギフト情報(受け取る側)
    membergiftreceive_lebelname: str  # 受け取ったメンバーシップギフトのレベル
    # ユーザー情報
    author_channel_id: str  # チャンネルID
    author_display_name: str  # 表示名
    author_is_verified: bool  # YouTubeに確認されているか否か
    author_is_chatowner: bool  # ライブチャットの所有者か否か
    author_is_chatsponsor: bool  # メンバーシップに入っているか否か
    author_is_chatmoderator: bool  # ライブチャットのモデレーターか否か
    # ban情報
    ban_channelid: str  # banされたユーザーのチャンネルID
    ban_display_name: str  # banされたユーザーのチャンネル表示名
