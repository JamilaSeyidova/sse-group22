# sse-group22

When running:
    streams = YouTube('https://www.youtube.com/watch?v=LXb3EKWsInQ').streams.filter(res=res, fps=fps,
                                                                                    mime_type=mime_type)
encountered this error: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1122)>

To fix download certificates. Example for Python 3.9: 
        "/Applications/Python\ 3.9/Install\ Certificates.command"