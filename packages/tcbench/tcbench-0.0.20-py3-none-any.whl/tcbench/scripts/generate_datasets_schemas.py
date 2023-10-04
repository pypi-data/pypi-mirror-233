#!/usr/bin/env python
# coding: utf-8

import pandas as pd


from tcbench.libtcdatasets.datasets_utils import load_parquet


def convert_dtype_to_str(
    dtypes, enforce_numpy_for=None, descriptions=None, enforce_list_for=None
):
    if enforce_numpy_for is None:
        enforce_numpy_for = []
    if enforce_list_for is None:
        enforce_list_for = []
    if descriptions is None:
        descriptions = {}

    lines = []
    for name, value in dtypes.items():
        if value.name.startswith("int"):
            value = "int"
        elif value.name.startswith("float"):
            value = "float"
        elif name in enforce_numpy_for:
            value = "np.array"
        elif name in enforce_list_for:
            value = "list"
        elif value.name == "object":
            value = "str"

        lines.append(f"{name}:")
        lines.append(f"   dtype: {value}")
        lines.append(f'   description: "{descriptions.get(name,"")}"')
    return lines


DESCRIPTIONS_GENERIC_SPLIT = dict(
    train_indexes="row_id of training samples",
    val_indexes="row_id of validation samples",
    test_indexes="row_id of test samples",
    split_index="Split id",
)
NUMPY_COLUMNS_GENERIC_SPLIT = ["train_indexes", "val_indexes", "test_indexes"]


UCDAVISICDM19_DESCRIPTIONS = dict(
    row_id="Unique row id",
    app="Label of the flow",
    flow_id="Original filename",
    partition="Partition related to the flow",
    num_pkts="Number of packets in the flow",
    duration="Duration of the flow",
    bytes="Number of bytes of the flow",
    unixtime="Absolute time of each packet",
    timetofirst="Delta between a packet the first packet of the flow",
    pkts_size="Packet size time series",
    pkts_dir="Packet direction time series",
    pkts_iat="Packet inter-arrival time series",
)
UCDAVISICDM19_NUMPY_COLUMNS = ["pkts_size", "pkts_dir", "pkts_iat", "timetofirst"]


UTMOBILENET21_DESCRIPTIONS = dict(
    row_id="Unique flow id",
    src_ip="Source ip of the flow",
    src_port="Source port of the flow",
    dst_ip="Destination ip of the flow",
    dst_port="Destination port of the flow",
    ip_proto="Protocol of the flow (TCP or UDP)",
    first="Timestamp of the first packet",
    last="Timestamp of the last packet",
    duration="Duration of the flow",
    packets="Number of packets in the flow",
    bytes="Number of bytes in the flow",
    partition="From which folder the flow was originally stored",
    location="Label originally provided by the dataset (see the related paper for details)",
    fname="Original filename where the packets of the flow come from",
    app="Final label of the flow, encoded as pandas category",
    pkts_size="Packet size time series",
    pkts_dir="Packet diretion time series",
    timetofirst="Delta between the each packet timestamp the first packet of the flow",
)
UTMOBILENET21_NUMPY_COLUMNS = ["pkts_size", "pkts_dir", "timetofirst"]


MIRAGE19_DESCRIPTIONS = dict(
    row_id="Unique flow id",
    conn_id="Flow 5-tuple",
    packet_data_src_port="Time series of the source ports",
    packet_data_dst_port="Time series of the destination ports",
    packet_data_packet_dir="Time series of pkts direction (0 or 1)",
    packet_data_l4_payload_bytes="Time series of payload pkts size",
    packet_data_iat="Time series of pkts inter arrival times",
    packet_data_tcp_win_size="Time series of TCP window size",
    packet_data_l4_raw_payload="List of list with each packet payload",
    flow_features_packet_length_biflow_min="Bidirectional min frame (i.e., pkt with headers) size",
    flow_features_packet_length_biflow_max="Bidirectional max frame size",
    flow_features_packet_length_biflow_mean="Bidirectional mean frame size",
    flow_features_packet_length_biflow_std="Bidirectional std frame size",
    flow_features_packet_length_biflow_var="Bidirectional variance frame size",
    flow_features_packet_length_biflow_mad="Bidirectional median absolute deviation frame size",
    flow_features_packet_length_biflow_skew="Bidirection skew frame size",
    flow_features_packet_length_biflow_kurtosis="Bidirectional kurtosi frame size",
    flow_features_packet_length_biflow_10_percentile="Bidirection 10%-ile of frame size",
    flow_features_packet_length_biflow_20_percentile="Bidirection 20%-ile of frame size",
    flow_features_packet_length_biflow_30_percentile="Bidirection 30%-ile of frame size",
    flow_features_packet_length_biflow_40_percentile="Bidirection 40%-ile of frame size",
    flow_features_packet_length_biflow_50_percentile="Bidirection 50%-ile of frame size",
    flow_features_packet_length_biflow_60_percentile="Bidirection 60%-le of frame size",
    flow_features_packet_length_biflow_70_percentile="Bidirection 70%-ile of frame size",
    flow_features_packet_length_biflow_80_percentile="Bidirection 80%-ile of frame size",
    flow_features_packet_length_biflow_90_percentile="Bidirection 90%-ile of frame size",
    flow_features_packet_length_upstream_flow_min="Upstream min frame (i.e., pkt with headers) size",
    flow_features_packet_length_upstream_flow_max="Upstream max frame size",
    flow_features_packet_length_upstream_flow_mean="Upstream mean frame size",
    flow_features_packet_length_upstream_flow_std="Upstream std frame size",
    flow_features_packet_length_upstream_flow_var="Upstream variance frame size",
    flow_features_packet_length_upstream_flow_mad="Upstream median absolute deviation frame size",
    flow_features_packet_length_upstream_flow_skew="Upstream skew frame size",
    flow_features_packet_length_upstream_flow_kurtosis="Upstream kurtosi frame size",
    flow_features_packet_length_upstream_flow_10_percentile="Upstream 10%-ile frame size",
    flow_features_packet_length_upstream_flow_20_percentile="Upstream 20%-ile frame size",
    flow_features_packet_length_upstream_flow_30_percentile="Upstream 30%-ile frame size",
    flow_features_packet_length_upstream_flow_40_percentile="Upstream 40%-ile frame size",
    flow_features_packet_length_upstream_flow_50_percentile="Upstream 50%-ile frame size",
    flow_features_packet_length_upstream_flow_60_percentile="Upstream 60%-ile frame size",
    flow_features_packet_length_upstream_flow_70_percentile="Upstream 70%-ile frame size",
    flow_features_packet_length_upstream_flow_80_percentile="Upstream 80%-ile frame size",
    flow_features_packet_length_upstream_flow_90_percentile="Upstream 90%-ile frame size",
    flow_features_packet_length_downstream_flow_min="Downstream min frame (i.e., pkt with headers) size",
    flow_features_packet_length_downstream_flow_max="Downstream max frame size",
    flow_features_packet_length_downstream_flow_mean="Downstream mean frame size",
    flow_features_packet_length_downstream_flow_std="Downstream std frame size",
    flow_features_packet_length_downstream_flow_var="Downstream variance frame size",
    flow_features_packet_length_downstream_flow_mad="Downstream max frame size",
    flow_features_packet_length_downstream_flow_skew="Downstream skew frame size",
    flow_features_packet_length_downstream_flow_kurtosis="Downstream kurtosi frame size",
    flow_features_packet_length_downstream_flow_10_percentile="Downstream 10%-ile frame size",
    flow_features_packet_length_downstream_flow_20_percentile="Downstream 20%-ile frame size",
    flow_features_packet_length_downstream_flow_30_percentile="Downstream 30%-ile frame size",
    flow_features_packet_length_downstream_flow_40_percentile="Downstream 40%-ile frame size",
    flow_features_packet_length_downstream_flow_50_percentile="Downstream 50%-ile frame size",
    flow_features_packet_length_downstream_flow_60_percentile="Downstream 60%-ile frame size",
    flow_features_packet_length_downstream_flow_70_percentile="Downstream 70%-ile frame size",
    flow_features_packet_length_downstream_flow_80_percentile="Downstream 80%-ile frame size",
    flow_features_packet_length_downstream_flow_90_percentile="Downstream 90%-ile frame size",
    flow_features_iat_biflow_min="Bidirectional min inter arrival time",
    flow_features_iat_biflow_max="Bidirectional max inter arrival time",
    flow_features_iat_biflow_mean="Bidirectional mean inter arrival time",
    flow_features_iat_biflow_std="Bidirectional std inter arrival time",
    flow_features_iat_biflow_var="Bidirectional variance inter arrival time",
    flow_features_iat_biflow_mad="Bidirectional median absolute deviation inter arrival time",
    flow_features_iat_biflow_skew="Bidirectional skew inter arrival time",
    flow_features_iat_biflow_kurtosis="Bidirectional kurtosi inter arrival time",
    flow_features_iat_biflow_10_percentile="Bidirectional 10%-tile inter arrival time",
    flow_features_iat_biflow_20_percentile="Bidirectional 20%-tile inter arrival time",
    flow_features_iat_biflow_30_percentile="Bidirectional 30%-tile inter arrival time",
    flow_features_iat_biflow_40_percentile="Bidirectional 40%-tile inter arrival time",
    flow_features_iat_biflow_50_percentile="Bidirectional 50%-tile inter arrival time",
    flow_features_iat_biflow_60_percentile="Bidirectional 60%-tile inter arrival time",
    flow_features_iat_biflow_70_percentile="Bidirectional 70%-tile inter arrival time",
    flow_features_iat_biflow_80_percentile="Bidirectional 80%-tile inter arrival time",
    flow_features_iat_biflow_90_percentile="Bidirectional 90%-tile inter arrival time",
    flow_features_iat_upstream_flow_min="Upstream min inter arrival time",
    flow_features_iat_upstream_flow_max="Upstream max inter arrival time",
    flow_features_iat_upstream_flow_mean="Upstream avg inter arrival time",
    flow_features_iat_upstream_flow_std="Upstream std inter arrival time",
    flow_features_iat_upstream_flow_var="Upstream variance inter arrival time",
    flow_features_iat_upstream_flow_mad="Upstream median absolute deviation inter arrival time",
    flow_features_iat_upstream_flow_skew="Upstream skew inter arrival time",
    flow_features_iat_upstream_flow_kurtosis="Upstream kurtosi inter arrival time",
    flow_features_iat_upstream_flow_10_percentile="Upstream 10%-ile inter arrival time",
    flow_features_iat_upstream_flow_20_percentile="Upstream 20%-ile inter arrival time",
    flow_features_iat_upstream_flow_30_percentile="Upstream 30%-ile inter arrival time",
    flow_features_iat_upstream_flow_40_percentile="Upstream 40%-ile inter arrival time",
    flow_features_iat_upstream_flow_50_percentile="Upstream 50%-ile inter arrival time",
    flow_features_iat_upstream_flow_60_percentile="Upstream 60%-ile inter arrival time",
    flow_features_iat_upstream_flow_70_percentile="Upstream 70%-ile inter arrival time",
    flow_features_iat_upstream_flow_80_percentile="Upstream 80%-ile inter arrival time",
    flow_features_iat_upstream_flow_90_percentile="Upstream 90%-ile inter arrival time",
    flow_features_iat_downstream_flow_min="Downstream min inter arrival time",
    flow_features_iat_downstream_flow_max="Downstream max inter arrival time",
    flow_features_iat_downstream_flow_mean="Downstream mean inter arrival time",
    flow_features_iat_downstream_flow_std="Downstream std inter arrival time",
    flow_features_iat_downstream_flow_var="Downstream variance inter arrival time",
    flow_features_iat_downstream_flow_mad="Downstream median absolute deviation inter arrival time",
    flow_features_iat_downstream_flow_skew="Downstream skew inter arrival time",
    flow_features_iat_downstream_flow_kurtosis="Downstream kurtosi inter arrival time",
    flow_features_iat_downstream_flow_10_percentile="Downstream 10%-ile inter arrival time",
    flow_features_iat_downstream_flow_20_percentile="Downstream 20%-ile inter arrival time",
    flow_features_iat_downstream_flow_30_percentile="Downstream 30%-ile inter arrival time",
    flow_features_iat_downstream_flow_40_percentile="Downstream 40%-ile inter arrival time",
    flow_features_iat_downstream_flow_50_percentile="Downstream 50%-ile inter arrival time",
    flow_features_iat_downstream_flow_60_percentile="Downstream 60%-ile inter arrival time",
    flow_features_iat_downstream_flow_70_percentile="Downstream 70%-ile inter arrival time",
    flow_features_iat_downstream_flow_80_percentile="Downstream 80%-ile inter arrival time",
    flow_features_iat_downstream_flow_90_percentile="Downstream 90%-ile inter arrival time",
    flow_metadata_bf_label="original mirage label",
    flow_metadata_bf_labeling_type="exact=via netstat; most-common=via experiment",
    flow_metadata_bf_num_packets="Bidirectional number of pkts",
    flow_metadata_bf_ip_packet_bytes="Bidirectional bytes (including headers)",
    flow_metadata_bf_l4_payload_bytes="Bidirectional payload bytes",
    flow_metadata_bf_duration="Bidirectional duration",
    flow_metadata_uf_num_packets="Upload number of pkts",
    flow_metadata_uf_ip_packet_bytes="Upload bytes (including headers)",
    flow_metadata_uf_l4_payload_bytes="Upload payload bytes",
    flow_metadata_uf_duration="Upload duration",
    flow_metadata_df_num_packets="Download number of packets",
    flow_metadata_df_ip_packet_bytes="Download bytes (including headers)",
    flow_metadata_df_l4_payload_bytes="Download payload bytes",
    flow_metadata_df_duration="Download duration",
    strings="ASCII string extracted from payload",
    android_name="app name (based on filename)",
    device_name="device name (based on filename)",
    app="label (background|android app)",
    src_ip="Source IP",
    src_port="Source port",
    dst_ip="Destination IP",
    dst_port="Destination port",
    proto="L4 protocol",
    packets="Number of (bidirectional) packets",
    ##########################
    ## EXTRAS added in filtered
    ##########################
    pkts_size="Packet size time series",
    pkts_dir="Packet diretion time series",
    timetofirst="Delta between the each packet timestamp the first packet of the flow",
)

MIRAGE19_NUMPY_COLUMNS = [
    "packet_data_src_port",
    "packet_data_dst_port",
    "packet_data_packet_dir",
    "packet_data_l4_payload_bytes",
    "packet_data_iat",
    "packet_data_tcp_win_size",
    "packet_data_l4_raw_payload",
]

MIRAGE19_LIST_COLUMNS = ["packet_data_l4_raw_payload", "strings"]


MIRAGE22_DESCRIPTIONS = MIRAGE19_DESCRIPTIONS.copy()
MIRAGE22_DESCRIPTIONS.update(
    dict(
        flow_metadata_bf_activity="Experiment activity",
        flow_metadata_bf_device="Ethernet address",
        flow_metadata_bf_label_source="Constant value 'netstate'",
        flow_metadata_bf_label_version_code="n.a.",
        flow_metadata_bf_label_version_name="n.a.",
        flow_metadata_bf_sublabel="n.a.",
        flow_metadata_df_mss="Download maximum segment size",
        flow_metadata_df_ws="Download window scaling",
        flow_metadata_uf_mss="Upload maximum segment size",
        flow_metadata_uf_ws="Upload window scaling",
        packet_data_annotations="n.a.",
        packet_data_heuristic="n.a.",
        packet_data_ip_header_bytes="Time series of IP header bytes",
        packet_data_ip_packet_bytes="Time series pkts bytes (as from IP len field)",
        packet_data_is_clear="n.a.",
        packet_data_l4_header_bytes="Time series of L4 header bytes",
        packet_data_tcp_flags="Time series of TCP flags",
        packet_data_timestamp="Time series of packet unixtime",
    )
)

MIRAGE22_NUMPY_COLUMNS = MIRAGE19_NUMPY_COLUMNS[:] + [
    "packet_data_ip_header_bytes",
    "packet_data_ip_packet_bytes",
    "packet_data_is_clear",
    "packet_data_l4_header_bytes",
    "packet_data_tcp_flags",
    "packet_data_timestamp",
]

MIRAGE22_LIST_COLUMNS = ["packet_data_l4_raw_payload", "strings"]


with open("./ucdavis-icdm19.yml", "w") as fout:
    df = load_parquet("ucdavis-icdm19", split="train")
    lines = convert_dtype_to_str(
        df.dtypes, UCDAVISICDM19_NUMPY_COLUMNS, UCDAVISICDM19_DESCRIPTIONS
    )
    print("__all__:", file=fout)
    for li in lines:
        print("   " + li, file=fout)


with open("./utmobilenet21.yml", "w") as fout:
    df = load_parquet("utmobilenet21", min_pkts=-1)

    ## unfiltered
    lines = convert_dtype_to_str(
        df.dtypes, UTMOBILENET21_NUMPY_COLUMNS, UTMOBILENET21_DESCRIPTIONS
    )
    print("__unfiltered__:", file=fout)
    for li in lines:
        print("   " + li, file=fout)

    ## filtered is the same as unfiltered
    print("", file=fout)
    print("__filtered__:", file=fout)
    for li in lines:
        print("   " + li, file=fout)

    ## splits
    df = load_parquet("utmobilenet21", min_pkts=10, split=True)
    lines = convert_dtype_to_str(
        df.dtypes, NUMPY_COLUMNS_GENERIC_SPLIT, DESCRIPTIONS_GENERIC_SPLIT
    )
    print("", file=fout)
    print("__splits__:", file=fout)
    for li in lines:
        print("   " + li, file=fout)


with open("./mirage19.yml", "w") as fout:
    ## unfiltered
    df = load_parquet("mirage19", min_pkts=-1)
    lines = convert_dtype_to_str(
        df.dtypes, MIRAGE19_NUMPY_COLUMNS, MIRAGE19_DESCRIPTIONS, MIRAGE19_LIST_COLUMNS
    )
    print("__unfiltered__:", file=fout)
    for li in lines:
        print("   " + li, file=fout)

    ## filtered is the same as unfiltered
    df = load_parquet("mirage19", min_pkts=10)
    lines = convert_dtype_to_str(
        df.dtypes, MIRAGE19_NUMPY_COLUMNS, MIRAGE19_DESCRIPTIONS, MIRAGE19_LIST_COLUMNS
    )
    print("", file=fout)
    print("__filtered__:", file=fout)
    for li in lines:
        print("   " + li, file=fout)

    ## splits
    df = load_parquet("mirage19", min_pkts=10, split=True)
    lines = convert_dtype_to_str(
        df.dtypes, NUMPY_COLUMNS_GENERIC_SPLIT, DESCRIPTIONS_GENERIC_SPLIT
    )
    print("", file=fout)
    print("__splits__:", file=fout)
    for li in lines:
        print("   " + li, file=fout)


with open("./mirage22.yml", "w") as fout:
    ## unfiltered
    df = load_parquet("mirage22", min_pkts=-1)
    lines = convert_dtype_to_str(
        df.dtypes, MIRAGE22_NUMPY_COLUMNS, MIRAGE22_DESCRIPTIONS, MIRAGE22_LIST_COLUMNS
    )
    print("__unfiltered__:", file=fout)
    for li in lines:
        print("   " + li, file=fout)

    ## filtered is the same as unfiltered
    df = load_parquet("mirage22", min_pkts=10)
    lines = convert_dtype_to_str(
        df.dtypes, MIRAGE22_NUMPY_COLUMNS, MIRAGE22_DESCRIPTIONS, MIRAGE22_LIST_COLUMNS
    )
    print("", file=fout)
    print("__filtered__:", file=fout)
    for li in lines:
        print("   " + li, file=fout)

    ## splits
    df = load_parquet("mirage22", min_pkts=10, split=True)
    lines = convert_dtype_to_str(
        df.dtypes, NUMPY_COLUMNS_GENERIC_SPLIT, DESCRIPTIONS_GENERIC_SPLIT
    )
    print("", file=fout)
    print("__splits__:", file=fout)
    for li in lines:
        print("   " + li, file=fout)
