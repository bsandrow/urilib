pct_encoded = r'%[0-9a-fA-F]{2}'
unreserved  = r'[\w.~-]'
sub_delims  = r'[!$&\'()*+,;=]'
gen_delims  = r'[:/?#[\]@]'

reserved    = r'(?:%s|%s)' % (sub_delims, gen_delims)
pchar       = r'(?:%s|%s|%s|:|@)' % (unreserved, pct_encoded, sub_delims)

query       = r'(?:%s|/|[?])*' % (pchar)
fragment    = r'(?:%s|/|[?])*' % (pchar)

segment       = r'(?:%s)*' % (pchar)
segment_nz    = r'(?:%s)+' % (pchar)
segment_nz_nc = r'(?:%s|%s|%s|@)+' % (unreserved, pct_encoded, sub_delims)

path_abempty  = r'(?:/%s)*'       % segment
path_absolute = r'(?:/(?:%s(?:/%s)*)*' % (segment_nz, segment)
path_noscheme = r'(?:%s(?:/%s)*)' % (segment_nz_nc, segment)
path_rootless = r'(?:%s(?:/%s)*'  % (segment_nz, segment)
path_empty    = r''
path          = r'%s|%s|%s|%s|%s' % (path_abempty, path_absolute, path_noscheme,
                                        path_rootless, path_empty)

dec_octet     = r'\d{1,3}' # FIXME
hexdigit      = r'[0-9a-fA-F]'
h16           = r'%s{4}'          % (hexdigit)
ipv4_address  = r'%s\.%s\.%s\.%s' % (dec_octet, dec_octet, dec_octet, dec_octet)
ls32          = r'(?:%s:%s|%s)'   % (h16, h16, ipv4_address)
ipv6_part     = r'(?:%s:)'        % (h16)
ipv6_address  = r'(?:%s{6}%s'     % (ipv6_part, ls32) # FIXME
ipvfuture     = r'' # FIXME
ip_literal    = r'\[(?:%s|%s)\]'  % (ipv6_address, ipvfuture)
reg_name      = r'(?:%s|%s|%s)'   % (unreserved, pct_encoded, sub_delims)
userinfo      = r'(?:%s|%s|%s|:)' % (unreserved, pct_encoded, sub_delims)
host          = r'(?:%s|%s|%s)'   % (ip_literal, ipv4_address, reg_name)
port          = r'\d'

scheme        = r'(?:[^\W\d_](?:[^\W_]|[+.\-])*)'
authority     = r'(?:%s@)?%s(?::%s)?' % (userinfo, host, port)
hier_part     = r'(?://%s%s|%s|%s|%s)'  % (authority, path_abempty, path_absolute,
                                            path_noscheme, path_empty)
uri           = r'%s:%s(?:[?]%s)(?:[#]%s)' % (scheme, hier_part, query, fragment)
relative_part = r'//%s%s|%s|%s|%s'         % (authority, path_abempty, path_absolute,
                                                path_noscheme, path_empty)
relative_ref  = r'%s(?:%s)?(?:%s)?'        % (relative_part, query, fragment)
uri_reference = r'(?:%s)|(?:%s)'           % (uri, relative_ref)
absolute_uri  = r'%s:%s(?:[?]%s)'          % (scheme, hier_part, query)

simple_uri_regex  = r'^(([^:/?#]+):)?((//([^/?#]*))?([^?#]*))?(\?([^#]*))?(#(.*))?'
