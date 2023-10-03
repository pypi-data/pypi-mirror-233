## Copyright (c) 2023 Blacknon. All rights reserved.
## Use of this source code is governed by an MIT license
## that can be found in the LICENSE file.
## =======================================================

## Macro
## =======================================================

## Template
## =======================================================

% This is the IRNIC Whois server v1.6.2.
% Available on web at http://whois.nic.ir/
% Find the terms and conditions of use on http://www.nic.ir/
%
% This server uses UTF-8 as the encoding for requests and responses.

% NOTE: This output has been filtered.

% Information related to 'google.ir'

<group>
domain:		{{ domain_name }}
ascii:		{{ ignore }}
nserver:	{{ name_servers | lower | ORPHRASE | to_list | joinmatches }}
source:		IRNIC # Filtered
</group>
